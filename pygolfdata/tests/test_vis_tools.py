"""
Unit tests functions in the vis_tools.py module

Classes:
    VisTests: Unit tests visualization functions in vis_tools.py
"""
import unittest

# pylint isn't seeing the shotlink module or models module here, while these tests run fine, so it's a false pos
from data import shotlink # pylint: disable=no-name-in-module
from models import vis_tools # pylint: disable=no-name-in-module


# DATA_PATH points to the full data, TEST_DATA_PATH to files w/ the same
# name but with a fraction of the rows, so tests run faster - as of this writing
# the content is the first 1000 rows of the full data
DATA_PATH = 'data'
TEST_DATA_PATH = 'data/test'

class VisTests(unittest.TestCase):
    '''Tests the two plotting functions in vis_tools.py

    Methods:
        setUp
        test_scatter
        test_heatmap
    '''
    def setUp(self):
        self.df = shotlink.get_combined_data_from_file(
            f'{TEST_DATA_PATH}/combined_shots_and_weather_2016_2016.csv')

    def test_scatter(self):
        '''Tests the scatter plotting function
        '''
        vis_tools.plot_strokes_gained_scatter(self.df, 'PrecipitationIntensity')

    def test_heatmap(self):
        '''Tests the heatmap function
        '''
        vis_tools.plot_heatmaps(self.df)

if __name__ == '__main__':
    unittest.main()
