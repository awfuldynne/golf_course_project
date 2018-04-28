import unittest

from data import shotlink

class ShotsTests(unittest.TestCase):

    def test_get_shots_has_2017_data(self):
        df = shotlink.get_shots([2017])
        self.assertEqual(1214437, len(df))

    def test_get_shots_has_two_years_worth_of_data(self):
        df = shotlink.get_shots([2008,2009])
        self.assertEqual(2343419, len(df))

    def test_get_shots_updates_colnames(self):
        df = shotlink.get_shots([2017])
        self.assertListEqual(shotlink.shot_fields, df.columns.values.tolist())
