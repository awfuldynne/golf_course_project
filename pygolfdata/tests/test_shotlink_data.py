import unittest

from data import shotlink

# DATA_PATH points to the full data, TEST_DATA_PATH to files w/ the same
# name but with a fraction of the rows, so tests run faster - as of this writing
# the content is the first 1000 rows of the full data
DATA_PATH = '../../golf_course_project_data'
TEST_DATA_PATH = '../../golf_course_project_data/test'

class ShotTests(unittest.TestCase):
    """Tests for shot data, generally using the data subsets in the data test directory, for speed."""
    def test_get_shots_has_2017_data(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        self.assertEqual(999, len(df))

    def test_get_shots_has_two_years_worth_of_data(self):
        df = shotlink.get_shots([2008,2009], TEST_DATA_PATH)
        self.assertEqual(999+999, len(df))

    def test_get_shots_updates_field_names(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        self.assertListEqual(list(shotlink.shot_dtypes.keys()), df.columns.values.tolist())
        #self.assertListEqual(shotlink.shot_fields, df.columns.values.tolist())

    def test_get_shots_has_explicit_data_types(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        for field_name, dtype in shotlink.shot_dtypes.items():
            self.assertEqual(dtype, df.dtypes[field_name])

    def test_prepare_data_converts_date_field(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        df = shotlink.prepare_shots(df)
        self.assertEqual('datetime64[ns]', str(df['Date'].dtype))

    def test_get_shots_augmented_has_course_level_data(self):
        # for now I'll only check a few columns - I don't know that we need all of them
        # when combining, but I'm guessing we could use these at least
        df = shotlink.get_shots_augmented([2017], TEST_DATA_PATH)
        self.assertIn('AMWindSpd', df.columns)
        self.assertIn('PMWindSpd', df.columns)
        self.assertIn('AMWindDir', df.columns)
        self.assertIn('PMWindDir', df.columns)

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

    # TODO check for no nulls, w/ test data



class ShotTestsIntegration(unittest.TestCase):
    """Tests for shot data, that take longer, including tests with actual data."""
    def test_get_shots_has_2017_actual_data(self):
        df = shotlink.get_shots([2017], DATA_PATH)
        self.assertEqual(1214437, len(df))

    # TODO check that we have no nulls after joining w/ augmented and all data - check here too w/ all data

class CourseLevelTests(unittest.TestCase):
    """Tests for course level data, generally using the data subsets in the data test directory, for speed."""
    def test_get_courselevels_has_2017_data(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        self.assertEqual(3438, len(df))

    def test_get_courselevels_has_two_years_worth_of_data(self):
        df = shotlink.get_shots([2008,2009], TEST_DATA_PATH)
        self.assertEqual(999+999, len(df))

    def test_get_courselevels_updates_field_names(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        self.assertListEqual(list(shotlink.courselevel_dtypes.keys()), df.columns.values.tolist())

    def test_get_courselevels_has_explicit_data_types(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        for field_name, dtype in shotlink.courselevel_dtypes.items():
            self.assertEqual(dtype, df.dtypes[field_name])


class CourseLevelIntegrationTests(unittest.TestCase):
    """Tests for course level data, that take longer, including tests with actual data."""
    def test_get_courselevels_has_2017_actual_data(self):
        df = shotlink.get_courselevels([2017], DATA_PATH)
        self.assertEqual(3438, len(df))

