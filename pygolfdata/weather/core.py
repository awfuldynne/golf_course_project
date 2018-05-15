""" pygolfdata - weather module

Provides an interface to maintain and update a pandas DataFrame containing hourly weather data.

Classes:
    WeatherDateApi
        Class that leverages the DarkSky API to extract hourly weather data per day. Manages a pandas DataFrame and
        also writes the DataFrame out to CSV to preserve already gathered weather data.
"""
import time
import os
import pandas as pd

from darksky import forecast


class WeatherDateApi:
    """
    Class to creates and manage a DataFrame of weather characteristics. Leverages the DarkSky API to retrieve historical
    weather data.

    DataFrame Columns:
    ['Date', 'Hour', 'Latitude', 'Longitude', 'Summary', 'DegreesFahrenheit', 'Humidity', 'Visibility', 'WindBearing',
    'WindGust', 'WindSpeed', "PrecipitationIntensity", "PrecipitationType"]
    """
    COLUMNS = ['Date', 'Hour', 'Latitude', 'Longitude', 'Summary', 'DegreesFahrenheit', 'Humidity', 'Visibility',
               'WindBearing', 'WindGust', 'WindSpeed', "PrecipitationIntensity", "PrecipitationType"]

    def __init__(self, api_key, weather_history_file_path):
        self.__api_key = api_key
        self.__file_path = weather_history_file_path

        if os.path.isfile(weather_history_file_path):
            self.__df = pd.read_csv(weather_history_file_path)
        else:
            self.__df = self.__create_new_dataframe()

    def get_api_key(self):
        """Returns current API key"""
        return self.__api_key

    def set_api_key(self, new_api_key):
        """Overwrites current API key and sets extractor to """
        self.__api_key = new_api_key

    def get_output_file_path(self):
        """Returns current output file path"""
        return self.__file_path

    def set_output_file_path(self, file_path):
        """Sets the output file path if the path is valid"""
        path_directory = os.path.dirname(file_path)

        if os.path.isdir(path_directory):
            self.__file_path = file_path
        else:
            raise ValueError("Directory of given file_path doesn't exist!")

    def get_weather_dataframe(self):
        """Returns current weather DataFrame"""
        return self.__df

    def append_weather_data(self, latitude, longitude, app_date, write_new_csv=False):
        """Function to append new weather data to the weather DataFrame.

        :param latitude: Floating point value representing latitude
        :param longitude: Floating point value representing longitude
        :param date: Datetime to retrieve weather data
        :param write_new_csv: Flag to update csv output after data is appended
        :return: Nothing
        """
        # Validate input
        if not (-90 <= latitude <= 90):
            raise ValueError('Latitude is outside the expected range')

        if not (-180 <= longitude <= 180):
            raise ValueError('Longitude is outside the expected range')

        if ((self.__df['Date'] == app_date.strftime('%Y-%m-%d'))
                & (self.__df['Latitude'] == latitude)
                & (self.__df['Longitude'] == longitude)).any():
            print("Ignoring request, data already exists")
        else:
            epoch_time = time.mktime(app_date.timetuple())

            # Retrieve data from DarkSky API
            response = self.__get_weather_json_darksky(latitude, longitude, epoch_time)
            daylight_savings_time_shift = self.__get_daylight_savings_time_shift(len(response['hourly']['data']))

            # Iterate through response and append to DataFrame
            for hour in range(0, len(response['hourly']['data'])):
                hour_of_day = hour \
                    if daylight_savings_time_shift == 0 or hour < 2 else hour + daylight_savings_time_shift
                self.__df = \
                    self.__df.append(
                        self.__get_weather_series_from_response(app_date.strftime('%Y-%m-%d'),
                                                                hour_of_day,
                                                                latitude,
                                                                longitude,
                                                                response['hourly']['data'][hour]),
                        ignore_index=True)

            # If write_new_csv is True, write out the updated DF
            if write_new_csv:
                self.__df.to_csv(self.__file_path, index=False)

        return self.__df

    def __create_new_dataframe(self):
        """ """
        df = pd.DataFrame(columns=self.COLUMNS)
        return df

    def __get_weather_json_darksky(self, latitude, longitude, epoch_time):
        """ Calls the DarkSky API with the given latitude, longitude and epoch time to retrieve historical weather data.

        :param latitude: Float value representing latitude
        :param longitude: Float value representing longitude
        :param epoch_time: Numeric value representing
        :return: A darksky.forecast.Forecast object

        """
        response = forecast(self.__api_key, latitude, longitude, int(epoch_time))
        return response

    def __get_weather_series_from_response(self, local_date, hour, latitude, longitude, response):
        """ """
        response_keys = response.keys()

        row_data = [local_date,
                    hour,
                    latitude,
                    longitude,
                    response['summary'] if 'summary' in response_keys else None,
                    response['temperature'] if 'temperature' in response_keys else None,
                    response['humidity'] if 'humidity' in response_keys else None,
                    response['visibility'] if 'visibility' in response_keys else None,
                    response['windBearing'] if 'windBearing' in response_keys else None,
                    response['windGust'] if 'windGust' in response_keys else None,
                    response['windSpeed'] if 'windSpeed' in response_keys else None,
                    response['precipIntensity'] if 'precipIntensity' in response_keys else None,
                    response['precipType'] if 'precipType' in response_keys else None]
        row = pd.Series(row_data, index=self.COLUMNS)
        return row

    def __get_daylight_savings_time_shift(self, length):
        """"""
        hour_shift = 0
        if length == 25:
            hour_shift = -1
        elif length == 23:
            hour_shift = 1
        return hour_shift
