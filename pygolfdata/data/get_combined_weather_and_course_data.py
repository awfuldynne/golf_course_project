"""
Script that combines the active_course_date.csv along with the
courses_geocoded.txt files to generate a combined set of data that includes
weather data for each hour of each day of a given tournament, where that
tournament is located (lat, long) and the name of the golf course the
tournament was played on.
"""

from datetime import date
import os

import pandas as pd

from weather import core  # pylint: disable=import-error

LOCAL_DATA_FOLDER = '../../../golf_course_project_data'
ACTIVE_COURSE_DATE_FILE_NAME = 'active_course_dates.csv'
COURSES_GEOCODE_FILE_NAME = 'courses_geocoded.txt'
FINAL_OUTPUT_FILE_NAME = 'pga_tour_weather_data.csv2'


def run():
    """Generate combined weather, course data, date data set"""

    # Change from the directory golf_course_project/pygolfdata/data to the
    # local repository of the golf_course_project_data. In our example,
    # golf_course_project and golf_course_project_data share the same folder.
    os.chdir(LOCAL_DATA_FOLDER)

    # Read in active course dates and course geolocation data
    tour_dates_df = pd.read_csv(ACTIVE_COURSE_DATE_FILE_NAME)
    course_location = pd.read_csv(COURSES_GEOCODE_FILE_NAME)

    # Standardize course geolocation columns
    course_location.columns = \
        ['Index',
         'CourseName',
         'Latitude',
         'Longitude',
         'Address']

    # Merge course dates and geolcation data together
    course_date_geoloc_df = \
        tour_dates_df.merge(course_location, on='CourseName', how='left')

    # Create WeatherDateAPI object
    wda = \
        core.WeatherDateApi(
            '53adfd0c8369b455fddb5f87955a1e0c',
            os.path.join(LOCAL_DATA_FOLDER, 'weather_data_05212018.csv'))

    # For each row in the course_date_geoloc_df, generate weather data
    for row in course_date_geoloc_df.itertuples():
        date_split = [int(x) for x in str(row.Date).split('-')]
        wda.append_weather_data(
            row.Latitude,
            row.Longitude,
            date(date_split[0], date_split[1], date_split[2]))

    # Write out the weather data to a csv file
    wda.write_dataframe_to_file()

    # Retrieve the weather DataFrame
    weather_data = wda.get_weather_dataframe()

    # From the course_date_geoloc_df, limit the number of columns
    course_date_geoloc_subset_df = \
        course_date_geoloc_df[['CourseName', 'Date', 'Latitude', 'Longitude']]

    # Merge the weather data and course_date_geoloc_subset DataFrames together
    output_df = \
        weather_data.merge(
            course_date_geoloc_subset_df,
            on=['Latitude', 'Longitude', "Date"],
            how='left')

    # Write out final result set
    output_df.to_csv(
        os.path.join(LOCAL_DATA_FOLDER, FINAL_OUTPUT_FILE_NAME),
        index=False)


if __name__ == "__main__":
    run()
