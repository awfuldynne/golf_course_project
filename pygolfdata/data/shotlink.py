import pandas as pd
import numpy as np

DATA_PATH = '../../golf_course_project_data'

shot_fields = [
    'TourCode', 'TourDescription', 'Year', 'TournamentNum', 'PlayerNum',
    'CourseNum', 'PermanentTournamentNum', 'PlayerFirstName',
    'PlayerLastName', 'Round', 'TournamentName', 'CourseName',
    'Hole', 'HoleScore', 'ParValue', 'Yardage', 'Shot',
    'ShotType', 'NumStrokes', 'FromLocationScorer',
    'FromLocationEnhanced', 'ToLocationScorer',
    'ToLocationEnhanced', 'Distance', 'DistanceToPin',
    'InTheHoleFlag', 'AroundTheGreenFlag', 'FirstPuttFlag',
    'DistanceToHoleAfterShot', 'Time', 'Lie', 'Elevation',
    'Slope', 'XCoordinate', 'YCoordinate', 'ZCoordinate',
    'DistanceFromCenter', 'DistanceFromEdge', 'Date', 'LeftRight',
    'StrokesGainedBaseline', 'StrokesGainedCategory',
    'RecoveryShot' ]

shot_dtypes = {
    "TourCode": "category",
    "TourDescription": "category",
    "Year": np.uint16,
    "TournamentNum": np.uint16,
    "PlayerNum": np.uint16,
    "CourseNum": np.uint16,
    "PermanentTournamentNum": np.uint16,
    "PlayerFirstName": "category",
    "PlayerLastName": "category",
    "Round": np.uint8,
    "TournamentName": "category",
    "CourseName": "category",
    "Hole": np.uint8,
    "HoleScore": np.float32,
    "ParValue": np.uint8,
    "Yardage": np.uint16,
    "Shot": np.uint8,
    "ShotType": "category",
    "NumStrokes": np.uint8,
    "FromLocationScorer": "category",
    "FromLocationEnhanced": object,
    "ToLocationScorer": "category",
    "ToLocationEnhanced": "category",
    "Distance": np.uint16,
    "DistanceToPin": np.uint16,
    "InTheHoleFlag": "category",
    "AroundTheGreenFlag": "category",
    "FirstPuttFlag": "category",
    "DistanceToHoleAfterShot": np.uint16,
    "Time": np.uint16,
    "Lie": "category",
    "Elevation": "category",
    "Slope":"category",
    "XCoordinate": object,
    "YCoordinate": object,
    "ZCoordinate": object,
    "DistanceFromCenter": np.uint16,
    "DistanceFromEdge": np.uint16,
    #"Date":datetime, use parse_dates on load
    "LeftRight": "category",
    "StrokesGainedBaseline": np.float32,
    "StrokesGainedCategory": "category",
    "RecoveryShot": "category" }


def get_shots(years, data_path):
    """
    Loads shot data.

    :param years: a sequence of integer year values for which data is desired; for
                  example [2017], or [2015, 2016], etc.
    :param data_path: path to the location of the Shot20xx.TXT source files.

    :return: a DataFrame containing a row per shot, for the specified year(s).
    """

    # need na_values as below because 'Hole Score' has double spaced empty values
    dfs = [pd.read_csv(f'{data_path}/Shot{year}.TXT',
                       sep=';', encoding='ISO-8859-1',
                       header=0, names=shot_fields,
                       dtype=shot_dtypes,
                       na_values='  ') for year in years]
    return pd.concat(dfs, ignore_index=True)

def prepare_shots(df):
    """
    Prepares/cleans shot data. For example:
    - Converts 'Date' field to datetime (takes a while, so we don't do it on load).

    :param df: shot data DataFrame.
    :return: Shot data DataFrame with cleaned fields.
    """
    df['Date'] = pd.to_datetime(df['Date'])

    return df