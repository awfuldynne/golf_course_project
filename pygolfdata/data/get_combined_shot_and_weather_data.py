from datetime import datetime

import pandas as pd

import shotlink


def main():
    data_path = '../../../golf_course_project_data'
    # years = [2017]
    years = range(2012, 2017)

    print(f'Started at {datetime.now()}.')
    weather = pd.read_csv(f'{data_path}/pga_tour_weather_data.csv')
    print(f'Loaded weather data with {len(weather)} rows and {len(weather.columns)} columns.')

    # interim fix for a few rows w/ hour values of 24
    weather = weather[weather['Hour'] != 24]

    weather['WeatherDateAndHour'] = pd.to_datetime(weather['Date'] + ' ' + weather['Hour'].astype(str).str.zfill(2))

    shots = shotlink.get_shots_augmented(years, data_path)
    shots = shotlink.prepare_shots(shots)
    print(f'Loaded and prepared shot data with {len(shots)} rows and {len(shots.columns)} columns.')

    # merge_asof requires sorted keys
    shots.sort_values(by=['ShotDateAndTime'], inplace=True)
    weather.sort_values(by=['WeatherDateAndHour'], inplace=True)

    combined = pd.merge_asof(shots, weather, left_on='ShotDateAndTime', right_on='WeatherDateAndHour',
                             suffixes=['_shots', '_weather'], direction='nearest')
    combined['TimeDifference'] = combined['ShotDateAndTime'] - combined['WeatherDateAndHour']

    print(f'Writing {len(combined)} rows with {len(combined.columns)} columns...')
    combined.to_csv('combined_shots_and_weather.csv', index=False)
    print(f'Done at {datetime.now()}.')

if __name__ == '__main__':
    main()