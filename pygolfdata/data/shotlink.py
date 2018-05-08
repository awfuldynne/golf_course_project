import collections

import pandas as pd
import numpy as np

DATA_PATH = '../../golf_course_project_data'

shot_dtypes = collections.OrderedDict({
    'TourCode': 'category',
    'TourDescription': 'category',
    'Year': np.uint16,
    'TournamentNum': np.uint16,
    'PlayerNum': np.uint16,
    'CourseNum': np.uint16,
    'PermanentTournamentNum': np.uint16,
    'PlayerFirstName': 'category',
    'PlayerLastName': 'category',
    'Round': np.uint8,
    'TournamentName': 'category',
    'CourseName': 'category',
    'Hole': np.uint8,
    'HoleScore': np.float32,
    'ParValue': np.uint8,
    'Yardage': np.uint16,
    'Shot': np.uint8,
    'ShotType': 'category',
    'NumStrokes': np.uint8,
    'FromLocationScorer': 'category',
    'FromLocationEnhanced': object,
    'ToLocationScorer': 'category',
    'ToLocationEnhanced': 'category',
    'Distance': np.uint16,
    'DistanceToPin': np.uint16,
    'InTheHoleFlag': 'category',
    'AroundTheGreenFlag': 'category',
    'FirstPuttFlag': 'category',
    'DistanceToHoleAfterShot': np.uint16,
    'Time': np.uint16,
    'Lie': 'category',
    'Elevation': 'category',
    'Slope':'category',
    'XCoordinate': object,
    'YCoordinate': object,
    'ZCoordinate': object,
    'DistanceFromCenter': np.uint16,
    'DistanceFromEdge': np.uint16,
    'Date': object, # use parse_dates while preparing; takes too long to do on read_csv
    'LeftRight': 'category',
    'StrokesGainedBaseline': np.float32,
    'StrokesGainedCategory': 'category',
    'RecoveryShot': 'category' })

# size of the source dataframe is much less than shots, but I'll set dtypes explicitly
# since we'll be pulling this data into a joined dataframe
courselevel_dtypes = collections.OrderedDict({
    'Year': np.uint16,
    'CourseNum': np.uint16,
    'CourseName': 'category',
    'Round': np.uint8,
    'Hole': np.uint8,
    'FwyWidth250': np.uint16,
    'Actual250Distance': np.uint16,
    'FwyWidth275': np.uint16,
    'Actual275Distance': np.uint16,
    'FwyWidth300': np.uint16,
    'Actual300Distance': np.uint16,
    'FwyWidth325': np.uint16,
    'Actual325 Distance': np.uint16,
    'FwyWidth350': np.uint16,
    'Actual350Distance': np.uint16,
    'FwyFirmness': 'category',
    'GrnFirmness': 'category',
    'GrnHeight': np.float32,
    'RoughHeight': np.float32,
    'FwyHeight': np.float32,
    'Stimp': 'category',
    'AMWindSpd': 'category',
    'AMWindDir': 'category',
    'PMWindSpd': 'category',
    'PMWindDir': 'category',
    'ScorecardYdg': np.uint16,
    'ActualYdg': np.float32, # has some NaNs
    'Par': np.uint8,
    'GreenGrass': 'category',
    'FwyGrass': 'category',
    'TeeGrass': 'category',
    'BunkerGrass': 'category',
    'RoughGrass': 'category',
    'ExtraColumn': object})


def get_years(type_prefix, data_path, years, **kwargs):
    """Module internal function to retrieve specified data; called by get_shots, etc."""
    dfs = [pd.read_csv(f'{data_path}/{type_prefix}{year}.TXT',
                       sep=';', encoding='ISO-8859-1', **kwargs) for year in years]
    return pd.concat(dfs, ignore_index=True)

def get_shots(years, data_path):
    """
    Loads shot data.

    :param years: a sequence of integer year values for which data is desired; for
                  example [2017], or [2015, 2016], etc.
    :param data_path: path to the location of the Shot20xx.TXT source files.

    :return: a DataFrame containing a row per shot, for the specified year(s).
    """
    # need na_values as below because 'Hole Score' has double spaced empty values
    return get_years('Shot', data_path, years,
                     header=0, names=shot_dtypes.keys(),
                     dtype=shot_dtypes,
                     na_values='  ')

def get_shots_augmented(years, data_path):
    """
    Loads shot data, augmented with data from other exports - for now, with weather
    data from the 'courselevels' export.

    :param years: a sequence of integer year values for which data is desired; for
                  example [2017], or [2015, 2016], etc.
    :param data_path: path to the location of the Shot20xx.TXT source files.

    :return: a DataFrame containing a row per shot, for the specified year(s).
    """
    shots = get_shots(years, data_path)
    courselevels = get_courselevels(years, data_path)

    courselevels_cols_to_keep = ['AMWindSpd', 'PMWindSpd', 'AMWindDir', 'PMWindDir',
                                 'Year', 'CourseNum', 'Round', 'Hole']

    # I think CourseNum captures the tournament, for courses that have multiple tournaments
    # (per the shot detail field def doc, 'courses played in more than one event will receive
    #  a number for each event), so we don't need to join on something tournament-related
    df=pd.merge(shots, courselevels[courselevels_cols_to_keep],
                how='left', on=['Year', 'CourseNum', 'Round', 'Hole'])
    return df


def prepare_shots(df):
    """
    Prepares/cleans shot data. For example:
    - Converts 'Date' field to datetime (takes a while, so we don't do it on load).

    :param df: shot data DataFrame.
    :return: Shot data DataFrame with cleaned fields.
    """
    df['Date'] = pd.to_datetime(df['Date'])

    return df


def get_courselevels(years, data_path):
    """
    Loads course level data.

    Course level data has a bunch of data that could correlate with performance (fairway width, firmness,
    grass height, stimpmeter, as well as recorded wind data that we might be able to use in comparison
    to the wind data we get separately.

    :param years: a sequence of integer year values for which data is desired; for
                  example [2017], or [2015, 2016], etc.
    :param data_path: path to the location of the source files.

    :return: a DataFrame containing a row per course level, for the specified year(s).
    """
    return get_years('CourseLevel', data_path, years,
                     header=0, names=courselevel_dtypes.keys(), dtype=courselevel_dtypes)


def get_specific_shot(df, last_name, first_name, year, tournament, course, round, hole, shot):
    """Convenience method to get a single row/shot. df is a dataframe with shot data."""
    return df[(df['PlayerLastName'] == last_name) &
              (df['PlayerFirstName'] == first_name) &
              (df['Year'] == year) &
              (df['TournamentName'] == tournament) &
              (df['CourseName'] == course) &
              (df['Round'] == round) &
              (df['Hole'] == hole) &
              (df['Shot'] == shot)].iloc[0]  # TODO exception/something if more than one row?