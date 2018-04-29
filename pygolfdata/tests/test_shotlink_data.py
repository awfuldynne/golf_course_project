import unittest

from data import shotlink


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
        self.assertListEqual(shotlink.shot_fields, df.columns.values.tolist())

    def test_get_shots_has_explicit_data_types(self):
        df = shotlink.get_shots([2017], TEST_DATA_PATH)
        for field_name, dtype in shotlink.shot_dtypes.items():
            self.assertEqual(dtype, df.dtypes[field_name])


class ShotTestsIntegration(unittest.TestCase):
    """Tests for shot data, that take longer, including tests with actual data."""
    def test_get_shots_has_2017_actual_data(self):
        df = shotlink.get_shots([2017])
        self.assertEqual(1214437, len(df))
