""" pygolfdata - weather module

Provides an interface to maintain and update a pandas DataFrame containing hourly weather data.

Classes:
    WeatherDateApi
        Class that leverages the DarkSky API to extract hourly weather data per day. Manages a pandas DataFrame and
        also writes the DataFrame out to CSV to preserve already gathered weather data.
"""
from datetime import datetime
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
    'WindGust', 'WindSpeed']
    """
    COLUMNS = ['Date', 'Hour', 'Latitude', 'Longitude', 'Summary', 'DegreesFahrenheit', 'Humidity', 'Visibility',
               'WindBearing', 'WindGust', 'WindSpeed', "PrecipitationIntensity", "PrecipitationType"]

    def __init__ (self, api_key, weather_history_file_path):
        self.__api_key = api_key
        self.__file_path = weather_history_file_path

        if os.path.isfile(weather_history_file_path):
            self.__df = pd.read_csv(weather_history_file_path)
        else:
            self.__df = self.__create_new_dataframe()

    def get_api_key(self):
        return self.__api_key

    def set_api_key(self, new_api_key):
        """Overwrites current API key and sets extractor to """
        self.__api_key = new_api_key

    def get_weather_dataframe(self):
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

        epoch_time = time.mktime(app_date.timetuple())

        # Retrieve data from DarkSky API
        response = self.__get_weather_json_darksky(latitude, longitude, epoch_time)

        # Iterate through response and append to DataFrame
        for hourly_snapshot in response['hourly']['data']:
            self.__df =\
                self.__df.append(self.__get_weather_series_from_response(latitude, longitude, hourly_snapshot),
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
        """ """
        response = forecast(self.__api_key, latitude, longitude, int(epoch_time))
        return response

    def __get_weather_series_from_response(self, latitude, longitude, response):
        """ """
        print(response)
        response_keys = response.keys()

        date_time = datetime.fromtimestamp(response['time'])
        row_data = [date_time.strftime('%Y-%m-%d'),
                    date_time.hour,
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
