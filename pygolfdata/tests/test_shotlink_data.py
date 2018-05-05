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


class ShotTestsIntegration(unittest.TestCase):
    """Tests for shot data, that take longer, including tests with actual data."""
    def test_get_shots_has_2017_actual_data(self):
        df = shotlink.get_shots([2017], DATA_PATH)
        self.assertEqual(1214437, len(df))


class CourseLevelTests(unittest.TestCase):
    """Tests for course level data, generally using the data subsets in the data test directory, for speed."""
    def test_get_courselevels_has_2017_data(self):
        df = shotlink.get_courselevels([2017], TEST_DATA_PATH)
        self.assertEqual(999, len(df))

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