"""
Obtains the latitude and longitude for each course, outputting the result to a file called
courses_geocoded.txt.
"""
import zipfile
import pandas as pd
import requests

def get_unique_values_from_zip(zip_file, csv_file, field_num):
    ''' Function to read a compressed CSV file within a zip archive and extract
        unique values from a particular field, line by line, without unzipping.
        It will include the header in the result, if it exists.

    Args:
        zip_file (str): The path to the compressed zip file
        csv_file (str): The name of the CSV file within the archive
        field_num (int): the field to gather unique values, based on a zero-index array

    Returns:
        values: a Python set object containing the unique values found
    '''
    values = set([])
    with zipfile.ZipFile(zip_file, 'r') as zf:
        with zf.open(csv_file) as fh:
            for line in fh:
                value = str(line).split(',')[field_num]
                if value not in values:
                    values.add(value)
    return values


URL = "https://maps.googleapis.com/maps/api/geocode/json"

# This is my API key attached to my own credit card
API_KEY = 'insert_your_own_api_key_here'

# The file containing the golf course information
#archive = '../../../golf_course_project_data/combined2012to2016.zip'
ARCHIVE = '../golf_course_project_data/combined2012to2016.zip'
FILE_NAME = 'combined_shots_and_weather_2012_2016.csv'
FIELD_NAME = 'CourseName_shots'

# Extract the unique values directly from the 11th field in the zipped csv
courses = get_unique_values_from_zip(ARCHIVE, FILE_NAME, 11)
# Then remove the field name from the list of unique courses
courses.remove(FIELD_NAME)

latlong = []
results = None

for name in courses:
    params = {'key': API_KEY, 'address': name}
    print(name)
    r = requests.get(URL, params=params)
    results = r.json()['results']
    print(results)
    location = results[0]['geometry']['location']
    lat = location['lat']
    long = location['lng']
    formatted_address = results[0]['formatted_address']
    latlong.append([name, lat, long, formatted_address])

latlong_df = pd.DataFrame(data=latlong, columns=['name', 'lat', 'long', 'address'])

latlong_df.to_csv('courses_geocoded.txt')
