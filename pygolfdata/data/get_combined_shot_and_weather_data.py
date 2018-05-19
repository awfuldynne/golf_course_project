"""
Script that generates the ultimate combined data that we use for analysis, and then copies the
combined data to the data directory for immediate use. The code uses weather data already
retrieved, and combines it with shot/courselevel data from shotlink.get_shots_augmented. The
weather data joined with any particular row is the weather data for the closest hour to when
the shot in question was taken.
"""

from datetime import datetime
import zipfile
import shutil  # for copy file function copy2

import pandas as pd

import shotlink


def main():
    """Combined data and copy/zip output."""
    data_path = '../data'

    START_YEAR = 2012
    END_YEAR = 2016
    years = range(START_YEAR, END_YEAR + 1)

    print(f'Started at {datetime.now()}, for years {START_YEAR} to {END_YEAR}.')

    weather = pd.read_csv(f'{data_path}/pga_tour_weather_data.csv')
    print(f'Loaded weather data with {len(weather)} rows and {len(weather.columns)} columns.')

    # create datetime col from weather data, for join
    weather['WeatherDateAndHour'] = pd.to_datetime(weather['Date'] + ' ' +
                                                   weather['Hour'].astype(str).str.zfill(2))

    shots = shotlink.get_shots_augmented(years, data_path)
    shots = shotlink.prepare_shots(shots)
    print(f'Loaded and prepared shot data with {len(shots)} rows and {len(shots.columns)} columns.')

    # merge_asof requires sorted keys
    shots.sort_values(by=['ShotDateAndTime'], inplace=True)
    weather.sort_values(by=['WeatherDateAndHour'], inplace=True)

    combined = pd.merge_asof(shots, weather, left_on='ShotDateAndTime',
                             right_on='WeatherDateAndHour',
                             suffixes=['_shots', '_weather'],
                             direction='nearest')
    combined['TimeDifference'] = combined['ShotDateAndTime'] - combined['WeatherDateAndHour']

    csv_filename = f'combined_shots_and_weather_{START_YEAR}_{END_YEAR}.csv'
    print(f'Writing {len(combined)} rows with {len(combined.columns)} cols, to {csv_filename}...')
    combined.to_csv(csv_filename, index=False)

    # TODO this may need to change now that we've moved to a submodule for the data
    print('Zipping...')
    zip_filename = f'combined{START_YEAR}to{END_YEAR}.zip'
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        zip_ref.write(csv_filename)

    print('Copying...')
    # copy both csv and zip to data location, former allows immediate use on this machine w/o unzip
    shutil.copy2(csv_filename, data_path) # copy2 allows dest to be a dir (poorly named function)
    shutil.copy2(zip_filename, data_path)

    print(f'Done at {datetime.now()}.')

if __name__ == '__main__':
    main()
