"""
Obtains the latitude and longitude for each course, outputting the result to a file called
courses_geocoded.txt.
"""
import zipfile
import pandas as pd
import requests


def get_unique_values_from_zip(zip_file, csv_file, field_num):
    """ Function to read a compressed CSV file within a zip archive and extract
        unique values from a particular field, line by line, without unzipping.
        It will include the header in the result, if it exists.

    Args:
        zip_file (str): The path to the compressed zip file
        csv_file (str): The name of the CSV file within the archive
        field_num (int): the field to gather unique values, based on a zero-index array

    Returns:
        values: a Python set object containing the unique values found
    """
    values = set([])
    with zipfile.ZipFile(zip_file, 'r') as zf:
        with zf.open(csv_file) as fh:
            for line in fh:
                value = str(line).split(',')[field_num]
                if value not in values:
                    values.add(value)
    return values


def main():
    """ Main function to read a compressed CSV file within a zip archive and extract
            unique values from a particular field, line by line, without unzipping.
            It will include the header in the result, if it exists.

        Returns:
            will write out unique course names with latitude and longitude to csv file
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # This is my API key attached to my own credit card
    api_key = 'insert_your_own_api_key_here'

    # Get a list of unique course names, then send a separate request for each course.
    courses = get_unique_values_from_zip(
        zip_file='../../../golf_course_project_data/combined2012to2016.zip',
        csv_file='combined_shots_and_weather_2012_2016.csv',
        field_num=11)

    # Then remove the field name from the list of unique courses
    courses.remove('CourseName_shots')

    latlong = []

    for name in courses:
        params = {'key': api_key, 'address': name}
        print(name)
        request = requests.get(url, params=params)
        results = request.json()['results']
        print(results)
        location = results[0]['geometry']['location']
        lat = location['lat']
        long = location['lng']
        formatted_address = results[0]['formatted_address']
        latlong.append([name, lat, long, formatted_address])

    latlong_df = pd.DataFrame(data=latlong, columns=['name', 'lat', 'long', 'address'])

    latlong_df.to_csv('courses_geocoded.txt')

if __name__ == '__main__':
    main()
