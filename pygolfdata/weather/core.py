""" pygolfdata - weather module

Provides an interface to update and maintain a pandas DataFrame containing
hourly weather data.

Classes:
    WeatherDateApi
        Class that leverages the DarkSky API to extract hourly weather data
        per day. Manages a pandas DataFrame and also writes the DataFrame out
        to CSV to preserve already gathered weather data.
"""
import os

from darksky import forecast
import pandas as pd


class WeatherDateApi:
    """
    Class to create and manage a DataFrame of weather characteristics.
    Leverages the DarkSky API to retrieve historical weather data.

    Attributes:
        COLUMNS (list of strings): List of headers for the weather DataFrame
    """
    COLUMNS = [
        'Date',
        'Hour',
        'Latitude',
        'Longitude',
        'Summary',
        'DegreesFahrenheit',
        'Humidity',
        'Visibility',
        'WindBearing',
        'WindGust',
        'WindSpeed',
        "PrecipitationIntensity",
        "PrecipitationType"]

    def __init__(self, api_key, weather_history_file_path):
        """ Initializes a WeatherDateApi object set to a given API key and
        output file path. If the output file path already exists, the data
        will attempt to be read into the DataFrame. Raises a ValueError if the
        directory to the specified file path doesn't exist.

        :param api_key: String representing a DarkSkyAPI key
        :param weather_history_file_path: Local path to output the weather csv
        """
        self.__api_key = api_key
        path_directory = os.path.dirname(weather_history_file_path)

        if os.path.isdir(path_directory):
            self.__file_path = weather_history_file_path
        else:
            raise ValueError("Directory of given file_path doesn't exist!")

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

    def write_dataframe_to_file(self):
        """Writes the current DataFrame out to disk"""
        self.__df.to_csv(self.__file_path, index=False)

    def append_weather_data(
            self,
            latitude,
            longitude,
            app_date,
            write_new_csv=False):
        """Function to append new weather data to the weather DataFrame.

        :param latitude: Floating point value representing latitude
        :param longitude: Floating point value representing longitude
        :param app_date: Datetime to retrieve weather data
        :param write_new_csv: Flag to update csv output after data is appended
        """
        # Validate input
        if not -90 <= latitude <= 90:
            raise ValueError('Latitude is outside the expected range')

        if not -180 <= longitude <= 180:
            raise ValueError('Longitude is outside the expected range')

        if ((self.__df['Date'] == app_date.strftime('%Y-%m-%d'))
                & (self.__df['Latitude'] == latitude)
                & (self.__df['Longitude'] == longitude)).any():
            print("Ignoring request, data already exists")
        else:
            date_string = \
                self.__generate_api_date_string(
                    app_date.year,
                    app_date.month,
                    app_date.day)

            # Retrieve data from DarkSky API
            response = self.__get_weather_json_darksky(
                latitude,
                longitude,
                date_string)
            daylight_savings_time_shift = \
                self.__get_daylight_savings_time_shift(
                    len(response['hourly']['data']))

            # Iterate through response and append to DataFrame
            for hour in range(0, len(response['hourly']['data'])):
                hour_of_day = hour \
                    if daylight_savings_time_shift == 0 or hour < 2 \
                    else hour + daylight_savings_time_shift
                self.__df = \
                    self.__df.append(
                        self.__get_weather_series_from_response(
                            app_date.strftime('%Y-%m-%d'),
                            hour_of_day,
                            latitude,
                            longitude,
                            response['hourly']['data'][hour]),
                        ignore_index=True)

            # If write_new_csv is True, write out the updated DF
            if write_new_csv:
                self.__df.to_csv(self.__file_path, index=False)

    def __create_new_dataframe(self):
        """Initializes a new and empty DataFrame with the columns set to the
        WeatherDateAPIs list of columns."""
        df = pd.DataFrame(columns=self.COLUMNS)
        return df

    def __get_weather_json_darksky(self, latitude, longitude, date_string):
        """Calls the DarkSky API with the given latitude, longitude and epoch
        time to retrieve historical weather data.

        :param latitude: Float value representing latitude
        :param longitude: Float value representing longitude
        :param date_string: Date string in the format of 'YYYY-MM-DDT00:00:00'
        :return: A darksky.forecast.Forecast object
        """
        response = forecast(self.__api_key, latitude, longitude, date_string)
        return response

    # pylint: disable-msg=too-many-arguments
    def __get_weather_series_from_response(
            self,
            local_date,
            hour,
            latitude,
            longitude,
            response):
        """Formats an hourly set of data points from a response from the
        DarkSkyAPI into a pandas
        Series.

        :param local_date: Date string. Expected format 'YYYY-MM-DD'
        :param hour: Integer representation of the hour of the day
        :param latitude: Float value representing latitude
        :param longitude: Float value representing longitude
        :param response: DarkSkyAPI hourly data block object
        :return: pandas Series object to be appended to the DataFrame
        """
        row_data = [
            local_date,
            hour,
            latitude,
            longitude,
            self.__return_column_value('summary', response),
            self.__return_column_value('temperature', response),
            self.__return_column_value('humidity', response),
            self.__return_column_value('visibility', response),
            self.__return_column_value('windBearing', response),
            self.__return_column_value('windGust', response),
            self.__return_column_value('windSpeed', response),
            self.__return_column_value('precipIntensity', response),
            self.__return_column_value('precipType', response)]
        row = pd.Series(row_data, index=self.COLUMNS)
        return row

    @staticmethod
    def __return_column_value(key_name, response):
        response_keys = response.keys()
        return response[key_name] if key_name in response_keys else None

    @staticmethod
    def __generate_api_date_string(year, month, day):
        """Creates a date string that matches the DarkSkyAPI's expected format
        from the passed in year, month and day.

        :param year: Integer for the year
        :param month: Integer representation of the month of the year
        :param day: Integer representation of the day of the month
        :return: Returns a date string of the form 'YYYY-MM-DDT00:00:00'
        """
        month = month if len(str(month)) == 2 else "0{}".format(month)
        day = day if len(str(day)) == 2 else "0{}".format(day)
        return "{}-{}-{}T00:00:00".format(year, month, day)

    @staticmethod
    def __get_daylight_savings_time_shift(length):
        """Returns an hour shift value to accommodate the timezone change that
        occurs during daylight savings time.

        :param length: Length of DarkSky API hourly data object
        :return: Return integer value indicating daylight savings time shift
        """
        hour_shift = 0
        if length == 25:
            hour_shift = -1
        elif length == 23:
            hour_shift = 1
        return hour_shift
