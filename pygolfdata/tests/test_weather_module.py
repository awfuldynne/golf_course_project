""" Unit tests for pygolfdata weather module

This module validates the functionality of the WeatherDateApi class exposed
under core in the weather library.

Classes:
    WeatherDateApiTest(unittest.TestCase)
        Framework for testing the functionality of the WeatherDateApi class.
"""


from datetime import date
import os
import random
import string
import unittest

# pylint isn't seeing the weatjer module here, while these tests run fine
from weather import core  # pylint: disable=import-error


class WeatherDateApiTest(unittest.TestCase):
    """ Class of unit tests for the WeatherDateApi's core functionality
    """
    existing_valid_file_path = \
        "pygolfdata/weather/test_data/weather_date_api_test.csv"
    non_existing_valid_file_path = \
        "weather/test_data/weather_date_api_test2.csv"
    invalid_file_path = \
        "weather/test_data/BAD_DIRECTORY/weather_date_api_test.csv"

    def setUp(self):
        self.wda = \
            core.WeatherDateApi(
                os.environ["darksky_api_key"],
                self.existing_valid_file_path)
        self.wda2 = \
            core.WeatherDateApi("TEST", self.non_existing_valid_file_path)
        self.df = self.wda.get_weather_dataframe()

    def test_invalid_file_path(self):
        """ Tests that the __init__ method throws a ValueError when given a bad
        file path
        """
        self.assertRaises(
            ValueError,
            core.WeatherDateApi,
            "",
            self.invalid_file_path)

    def test_get_api_key(self):
        """ Tests the API key get method
        """
        self.assertEqual(os.environ["darksky_api_key"], self.wda.get_api_key())

    def test_set_api_key(self):
        """ Tests the API key set method
        """
        random_key = \
            ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        self.wda.set_api_key(random_key)
        self.assertEqual(random_key, self.wda.get_api_key())

    def test_get_file_path(self):
        """ Tests the file path get method
        """
        self.assertEqual(
            self.existing_valid_file_path,
            self.wda.get_output_file_path())

    def test_set_file_path(self):
        """ Tests the file path set method
        """
        self.wda.set_output_file_path(self.non_existing_valid_file_path)
        self.assertEqual(
            self.non_existing_valid_file_path,
            self.wda.get_output_file_path())

    def test_set_invalid_file_path(self):
        """ Tests that the file path set method throws a ValueError when given
        a bad file path
        """
        self.assertRaises(
            ValueError,
            self.wda.set_output_file_path,
            self.invalid_file_path)

    def test_invalid_latitude(self):
        """ Tests that the an invalid latitude raises a ValueError
        """
        self.assertRaises(
            ValueError,
            self.wda.append_weather_data,
            91,
            -156.64,
            date(2012, 1, 6))

    def test_invalid_longitude(self):
        """ Tests that the an invalid longitude raises a ValueError
        """
        self.assertRaises(
            ValueError,
            self.wda.append_weather_data,
            21.0068,
            -190.64,
            date(2012, 1, 6))

    def test_column_names(self):
        """ Tests that all expected columns exist in the DataFrame
        """
        columns = self.wda.COLUMNS

        for column in columns:
            self.assertTrue(column in self.df.columns)

    def test_dataframe_size(self):
        """ Tests that the read in test DataFrame is the correct size
        """
        rows = 73
        columns = 13
        self.assertEqual(rows, self.df.shape[0])
        self.assertEqual(columns, self.df.shape[1])

    def test_darksky_api_call(self):
        """ Tests that a call to the DarkSky API appends the expected amount
        of data"""
        self.wda.append_weather_data(21.0068, -156.64, date(2012, 1, 6))
        df = self.wda.get_weather_dataframe()
        rows = 97
        columns = 13
        self.assertEqual(rows, df.shape[0])
        self.assertEqual(columns, df.shape[1])

    def test_dataframe_write_to_disk(self):
        """ Tests that the write DataFrame method writes a file to disk
        """
        self.assertFalse(os.path.isfile(self.non_existing_valid_file_path))
        self.wda2.write_dataframe_to_file()
        self.assertTrue(os.path.isfile(self.non_existing_valid_file_path))
        os.remove(self.non_existing_valid_file_path)

