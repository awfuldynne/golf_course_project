"""
Obtains the latitude and longitude for each course, outputting the result to a file called
courses_geocoded.txt.
"""
import pandas as pd
import os
import requests

from pygolfdata.data import shotlink

fname = '../../../golf_course_project_data/combined2016to2016.zip'

# Get a list of unique course names
df = shotlink.get_combined_data_from_file(fname)
courses = df['Course Name'].unique()

url = "https://maps.googleapis.com/maps/api/geocode/json"

# This is my API key attached to my own credit card
api_key = 'insert_your_own_api_key_here'

latlong = []
results = None

for name in courses['Course Name']:
    params = {'key': api_key, 'address': name}
    print(name)
    r = requests.get(url, params=params)
    results = r.json()['results']
    print(results)
    location = results[0]['geometry']['location']
    lat = location['lat']
    long = location['lng']
    formatted_address = results[0]['formatted_address']
    latlong.append([name, lat, long, formatted_address])

latlong_df = pd.DataFrame(data=latlong, columns=['name','lat','long','address'])

latlong_df.to_csv(PATH + 'courses_geocoded.txt')


