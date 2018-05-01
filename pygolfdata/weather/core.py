""" golf_course_project - weather module

Provides an interface to maintain and update a pandas DataFrame containing
hourly weather data.
"""
import arrow
import json
import pandas as pd
from WunderWeather import weather


class WeatherDateApi:
    """
    TEST
    """

    def __init__ (self, api_key, weather_history_file_path=None):
        self.__api_key = api_key
        self.__outfile_path = weather_history_file_path
        self.__df = pd.read_csv(weather_history_file_path)
        self.__extractor = weather.Extract(api_key)

    def get_api_key(self):
        return self.__api_key

    def set_api_key(self, new_api_key):
        """Overwrites current API key and sets extractor to """
        self.__api_key = new_api_key
        self.__extractor = weather.Extract(self.__api_key)

    def get_weather_dataframe(self):
        return self.__df

    def append_weather_data(self, city, state, start_date, end_date, write_new_csv=False):
        """ """
        # Validate input
        # start_date, end_date valid dates?

        # Get response from API
        response = self.__get_weather_json("", "")

        # Iterate through response and clean

        # Append to DataFrame

        # If write_new_csv is True, write out the updated DF

        return None

    def __get_weather_json(self, location, date_string):
        """ """
        date = arrow.get(date_string, "YYYYMMDD")
        response = self.__extractor.date(location, date.format("YYYYMMDD"))
        json_response = None
        try:
            json_response = json.loads(response)
        except:
            print("Bad things have happened")
        return json_response
