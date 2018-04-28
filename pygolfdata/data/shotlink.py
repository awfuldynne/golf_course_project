import pandas as pd

DATA_PATH = '../../golf_course_project_data'

shot_fields = ['Tour Code', 'Tour Description', 'Year', 'Tourn.#', 'Player #',
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
              'Recovery Shot']

def get_shots(years, data_path=DATA_PATH):
    """
    Returns a dataframe containing a row per shot, for the specified year(s).

    years: a sequence of integer year values for which data is desired; for
           example [2017], or [2015, 2016], etc.
    data_path: path to the location of the Shot20xx.TXT source files.
    """
    dfs = [pd.read_csv(f'{data_path}/Shot{year}.TXT', sep=';', encoding='ISO-8859-1',
                       header=0, names=shot_fields) for year in years]
    return pd.concat(dfs, ignore_index=True)
