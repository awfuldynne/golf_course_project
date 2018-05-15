""" Unit tests for pygolfdata weather module

This module validates the functionality of the WeatherDateApi class exposed under core in the weather library.

Classes:
    WeatherDateApiTest(unittest.TestCase)
        Framework for testing the core functionality of the WeatherDateApi class.
"""


import unittest
from weather import core


class WeatherDateApiTest(unittest.TestCase):
    """ Class of unit tests for the WeatherDateApi's core functionality
    """
    valid_file_path = "../test_data/weather_date_api_test.csv"

    def test_column_names(self):
        """ Tests that the columns of the DataFrame are equivalent to the COLUMN constant in the WeatherDateApi class.
        """
        w = core.WeatherDateApi("", self.valid_file_path)
        df = w.get_weather_dataframe()
        # Tests that all column names are equivalent and in the same order
        self.assertTrue(len([x for x in df.columns == core.WeatherDateApi.COLUMNS if x]) == len(df.columns))


if __name__ == '__main__':
    unittest.main()

