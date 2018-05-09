""" pygolfdata - weather module

Provides an interface to maintain and update a pandas DataFrame containing hourly weather data.
"""
import time
import json
import os
import pandas as pd

from darksky import forecast
from WunderWeather import weather


class WeatherDateApi:
    """
    Class to creates and manage a DataFrame of weather characteristics. Leverages the DarkSky API to retrieve historical
    weather data.

    DataFrame Columns:
    ['Date', 'Hour', 'Summary', 'DegreesFahrenheit', 'Humidity', 'Visibility', 'WindBearing', 'WindGust', 'WindSpeed']
    """
    COLUMNS = ['Date', 'Hour', 'Summary', 'DegreesFahrenheit', 'Humidity', 'Visibility', 'WindBearing', 'WindGust',
               'WindSpeed']

    def __init__ (self, api_key, weather_history_file_path):
        self.__api_key = api_key
        self.__extractor = weather.Extract(api_key)
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
        self.__extractor = weather.Extract(self.__api_key)

    def get_weather_dataframe(self):
        return self.__df

    def append_weather_data(self, latitude, longitude, start_date, end_date, write_new_csv=False):
        """Function to append new weather data to the weather DataFrame.

        :param latitude: Floating point value representing latitude
        :param longitude: Floating point value representing longitude
        :param start_date: Starting date of date range
        :param end_date: Ending date of date range
        :param write_new_csv: Flag to update csv output after data is appended
        :return: Nothing
        """
        # Validate input
        if not (-90 <= latitude <= 90):
            raise ValueError('Latitude is outside the expected range')

        if not (-180 <= longitude <= 180):
            raise ValueError('Longitude is outside the expected range')

        start_epoch_time = time.mktime(start_date)
        end_epoch_time = time.mktime(end_date)

        # TODO: Add check to not retrieve data that is already a part of the DataFrame
        loop_epoch_time = start_epoch_time
        while loop_epoch_time <= end_epoch_time:
            # Get response from API
            response = self.__get_weather_json_darksky(latitude, longitude, loop_epoch_time)

            # Iterate through response and clean
            for hourly_snapshot in response['hourly']['data']:
                print(hourly_snapshot)

            # Append to DataFrame
            self.__df = self.__df.append(self.__get_weather_series_from_response, ignore_index=True)

            # This is an unsafe assumption but good enough for now
            # https://stackoverflow.com/questions/7552104/is-a-day-always-86-400-epoch-seconds-long
            loop_epoch_time += 86400

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
        response = forecast(self.__api_key, latitude, longitude, epoch_time)
        json_response = None
        try:
            json_response = json.loads(response)
        except:
            print('Bad things have happened')
        return json_response

    def __get_weather_series_from_response(self, response):
        """ """
        row_data = ['date', 0, response['summary'], response['temperature'], response['humidity'],
                    response['visibility'], response['windBearing'], response['windGust'], response['windSpeed']]
        row = pd.Series(row_data, index=self.COLUMNS)
        return row
