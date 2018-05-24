"""
Tests - both unit and integration - for the code in shotlink.py, which loads and prepares
PGA ShotLink data.
"""
import unittest
from datetime import datetime

import pandas as pd
import numpy as np

# pylint isn't seeing the shotlink module here, while these tests run fine, so it's a false pos
from data import shotlink # pylint: disable=no-name-in-module

# DATA_PATH points to the full data, TEST_DATA_PATH to files w/ the same
# name but with a fraction of the rows, so tests run faster - as of this writing
# the content is the first 1000 rows of the full data
DATA_PATH = 'data'
TEST_DATA_PATH = 'data/test'

# These tests have descriptive method names and also aren't meant to be called (except by a
# test framework), and so don't ALSO need method docstrings; I'm turning off the warning for this
# file (only).
# pylint: disable=missing-docstring

class ShotTests(unittest.TestCase):
    """Tests for shot data, using the data subsets in the data test directory, for speed."""
    def test_get_shots_has_2017_data(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        self.assertEqual(999, len(df))

    def test_get_shots_has_two_years_worth_of_data(self):
        df = shotlink.get_shots([2008, 2009], TEST_DATA_PATH)
        self.assertEqual(999 + 999, len(df))

    def test_get_shots_updates_field_names(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        self.assertListEqual(list(shotlink.SHOT_DTYPES.keys()), df.columns.values.tolist())

    def test_get_shots_has_explicit_data_types(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        for field_name, dtype in shotlink.SHOT_DTYPES.items():
            self.assertEqual(dtype, df.dtypes[field_name])

    def test_prepare_data_converts_date_field(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        df = shotlink.prepare_shots(df)
        self.assertEqual('datetime64[ns]', str(df['Date'].dtype))
        self.assertEqual(datetime(2016, 10, 13), df['Date'][0])

    def test_prepare_adds_combined_date_and_time(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        df = shotlink.prepare_shots(df)
        self.assertIn('ShotDateAndTime', df.columns)
        self.assertEqual(datetime(2016, 10, 13, 12, 41), df.iloc[0]['ShotDateAndTime'])

    def test_prepare_adds_combined_player_name(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        df = shotlink.prepare_shots(df)
        self.assertEqual('Phil Mickelson', df.iloc[0]['PlayerName'])
        self.assertEqual('Charles Howell III', df.iloc[998]['PlayerName'])

    def test_get_shots_augmented_has_course_level_data(self):
        # for now I'll only check a few columns - I don't know that we need all of them
        # when combining, but I'm guessing we could use these at least
        df = shotlink.get_shots_augmented([2017], TEST_DATA_PATH)
        self.assertIn('AMWindSpd', df.columns)
        self.assertIn('PMWindSpd', df.columns)
        self.assertIn('AMWindDir', df.columns)
        self.assertIn('PMWindDir', df.columns)
        # I'd rather call assertIn once with a list of strings to reduce duplication, but when I do
        # I can't see which of the four fails, if one fails; instead I'll call each explicitly

    def test_get_shots_augmented_joins_correctly(self):
        # just check a few of the joins
        df = shotlink.get_shots_augmented([2017], TEST_DATA_PATH)
        phil = shotlink.get_specific_shot(df, 'Mickelson', 'Phil', 2017, 'Safeway Open',
                                          'Silverado Resort and Spa North', 1, 1, 1)
        self.assertEqual(' C', phil['AMWindSpd'])
        self.assertEqual('C', phil['AMWindDir'])
        self.assertEqual(' 5-10', phil['PMWindSpd'])
        self.assertEqual('DW', phil['PMWindDir'])
        ted = shotlink.get_specific_shot(df, 'Purdy', 'Ted', 2017, 'Safeway Open',
                                         'Silverado Resort and Spa North', 1, 16, 4)
        self.assertEqual(' C', ted['AMWindSpd'])
        self.assertEqual('C', ted['AMWindDir'])
        self.assertEqual(' 5-10', ted['PMWindSpd'])
        self.assertEqual('IW', ted['PMWindDir'])

    def test_get_shots_augmented_has_courselevels_for_all_rows(self):
        df = shotlink.get_shots_augmented([2017], TEST_DATA_PATH)
        self.assertEqual(0, sum(df['AMWindSpd'].isnull()))
        self.assertEqual(0, sum(df['AMWindDir'].isnull()))
        self.assertEqual(0, sum(df['PMWindSpd'].isnull()))
        self.assertEqual(0, sum(df['PMWindDir'].isnull()))
        # I'd rather do the following, to reduce duplication, but when I do I can't
        # see which of the four fails, if one fails
        # for field in ['AMWindSpd', 'AMWindDir', 'PMWindSpd', 'PMWindDir']:
        #    self.assertEqual(0, sum(df[field].isnull()))

    def test_get_active_course_dates(self):
        df = shotlink.get_active_course_dates([2017], TEST_DATA_PATH)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(1, len(df))
        self.assertEqual('Silverado Resort and Spa North', df.iloc[0]['CourseName'])
        self.assertEqual(datetime(2016, 10, 13), df.iloc[0]['Date'])

    def test_module_has_combined_dtypes(self):
        # check a few selected fields, not all
        self.assertIn('PlayerFirstName', shotlink.COMBINED_DTYPES.keys())
        self.assertEqual('category', shotlink.COMBINED_DTYPES['PlayerFirstName'])
        self.assertIn('PlayerName', shotlink.COMBINED_DTYPES.keys())
        self.assertEqual('category', shotlink.COMBINED_DTYPES['PlayerName'])
        self.assertIn('DegreesFahrenheit', shotlink.COMBINED_DTYPES.keys())
        self.assertEqual(np.float32, shotlink.COMBINED_DTYPES['DegreesFahrenheit'])

    def test_combined_data_from_file_and_dtypes(self):
        df = shotlink.get_combined_data_from_file(
            f'{TEST_DATA_PATH}/combined_shots_and_weather_2016_2016.csv')
        # test selected columns are ok w/ data types
        self.assertEqual('datetime64[ns]', str(df['WeatherDateAndHour'].dtype))
        self.assertEqual('float32', str(df['Humidity'].dtype))
        self.assertEqual('category', str(df['PlayerName'].dtype))
        self.assertEqual('uint8', str(df['Shot'].dtype))

    def test_get_specific_shot_raises_exception_for_no_shot(self):
        df = shotlink.get_shots([2017], DATA_PATH)
        self.assertRaises(ValueError, shotlink.get_specific_shot, df, 'foo', 'bar', 2017,
                          'foo', 'bar', 1, 1, 1)


class ShotTestsIntegration(unittest.TestCase):
    """Tests for shot data, that take longer, including tests with actual data."""
    def test_get_shots_has_2017_actual_data(self):
        df = shotlink.get_shots([2017], DATA_PATH)
        self.assertEqual(1214437, len(df))

    def test_get_shots_augmented_has_courselevels_for_all_possible_rows(self):
        # the courselevels data for 2017 doesn't have wind data for every single possible
        # course - at a quick glance, there are rows but no wind data for Erin Hills,
        # and for four tournaments where some of the initial rounds are played on multiple
        # course (for ex, the Pebble Beach Pro-Am, which is played on three courses at
        # least, I think, for the first two days) there are no courselevels rows at all
        # for the courses that are only used on Thursday and Friday; for now I'll just
        # hardcode the expected nulls that I got from separate investigation
        df = shotlink.get_shots_augmented([2017], DATA_PATH)
        self.assertEqual(99027, sum(df['AMWindSpd'].isnull()))
        self.assertEqual(99027, sum(df['AMWindDir'].isnull()))
        self.assertEqual(99027, sum(df['PMWindSpd'].isnull()))
        self.assertEqual(99430, sum(df['PMWindDir'].isnull()))

    # this one takes a long time because prepare_data takes a long time (because converting
    # the text dates to datetime instances takes a long time)
    def test_get_active_course_dates(self):
        df = shotlink.get_active_course_dates([2017], DATA_PATH)
        self.assertEqual(183, len(df))
        self.assertEqual(48, len(df['CourseName'].unique()))

    def test_prepare_data_fixes_fred_funk_bad_date(self):
        # the 2011 data has one row with a 12/30/1899 date that should be 3/3/2011
        df = shotlink.get_shots([2011], DATA_PATH)
        df = shotlink.prepare_shots(df)
        fred = shotlink.get_specific_shot(df, 'Funk', 'Fred', 2011, 'The Honda Classic',
                                          'PGA National (Champion)', 1, 1, 1)
        self.assertEqual(datetime(2011, 3, 3), fred['Date'])


class CourseLevelTests(unittest.TestCase):
    """Tests for course level data, using the data subsets in the data test directory, for speed."""
    def test_get_courselevels_has_2017_data(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        self.assertEqual(3438, len(df))

    def test_get_courselevels_has_two_years_worth_of_data(self):
        df = shotlink.get_shots([2008, 2009], TEST_DATA_PATH)
        self.assertEqual(999 + 999, len(df))

    def test_get_courselevels_updates_field_names(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        self.assertListEqual(list(shotlink.COURSELEVEL_DTYPES.keys()), df.columns.values.tolist())

    def test_get_courselevels_has_explicit_data_types(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        for field_name, dtype in shotlink.COURSELEVEL_DTYPES.items():
            self.assertEqual(dtype, df.dtypes[field_name])


class CourseLevelIntegrationTests(unittest.TestCase):
    """Tests for course level data, that take longer, including tests with actual data."""
    def test_get_courselevels_has_2017_actual_data(self):
        df = shotlink.get_courselevels([2017], DATA_PATH)
        self.assertEqual(3438, len(df))
