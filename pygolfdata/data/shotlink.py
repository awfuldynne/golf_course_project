import pandas as pd
import numpy as np

DATA_PATH = '../../golf_course_project_data'

shot_fields = [
    'Tour Code', 'Tour Description', 'Year', 'Tourn.#', 'Player #',
    'Course #', 'Permanent Tournament #', 'Player First Name',
    'Player Last Name', 'Round', 'Tournament Name', 'Course Name',
    'Hole', 'Hole Score', 'Par Value', 'Yardage', 'Shot',
    'Shot Type(S/P/D)', '# of Strokes', 'From Location(Scorer)',
    'From Location(Enhanced)', 'To Location(Scorer)',
    'To Location(Enhanced)', 'Distance', 'Distance to Pin',
    'In the Hole Flag', 'Around the Green Flag', '1st Putt Flag',
    'Distance to Hole after the Shot', 'Time', 'Lie', 'Elevation',
    'Slope', 'X Coordinate', 'Y Coordinate', 'Z Coordinate',
    'Distance from Center', 'Distance from Edge', 'Date', 'Left/Right',
    'Strokes Gained/Baseline', 'Strokes Gained Category',
    'Recovery Shot' ]

shot_dtypes = {
    "Tour Code":"category",
    "Tour Description":"category",
    "Year": np.uint16,
    "Tourn.#": np.uint16,
    "Player #": np.uint16,
    "Course #": np.uint16,
    "Permanent Tournament #": np.uint16,
    "Player First Name":"category",
    "Player Last Name":"category",
    "Round": np.uint8,
    "Tournament Name":"category",
    "Course Name":"category",
    "Hole": np.uint8,
    "Hole Score": np.float32,
    "Par Value": np.uint8,
    "Yardage": np.uint16,
    "Shot": np.uint8,
    "Shot Type(S/P/D)":"category",
    "# of Strokes": np.uint8,
    "From Location(Scorer)":"category",
    "From Location(Enhanced)": object,
    "To Location(Scorer)":"category",
    "To Location(Enhanced)":"category",
    "Distance": np.uint16,
    "Distance to Pin": np.uint16,
    "In the Hole Flag":"category",
    "Around the Green Flag":"category",
    "1st Putt Flag":"category",
    "Distance to Hole after the Shot": np.uint16,
    "Time": np.uint16,
    "Lie":"category",
    "Elevation":"category",
    "Slope":"category",
    "X Coordinate": object,
    "Y Coordinate": object,
    "Z Coordinate": object,
    "Distance from Center": np.uint16,
    "Distance from Edge": np.uint16,
    #"Date":datetime, use parse_dates on load
    "Left/Right":"category",
    "Strokes Gained/Baseline": np.float32,
    "Strokes Gained Category":"category",
    "Recovery Shot":"category" }


def get_shots(years, data_path=DATA_PATH):
    """
    Returns a dataframe containing a row per shot, for the specified year(s).

    years: a sequence of integer year values for which data is desired; for
           example [2017], or [2015, 2016], etc.
    data_path: path to the location of the Shot20xx.TXT source files.
    """

    # need na_values as below because 'Hole Score' has double spaced empty values
    dfs = [pd.read_csv(f'{data_path}/Shot{year}.TXT',
                       sep=';', encoding='ISO-8859-1',
                       header=0, names=shot_fields,
                       dtype=shot_dtypes,
                       na_values='  ') for year in years]
    return pd.concat(dfs, ignore_index=True)
