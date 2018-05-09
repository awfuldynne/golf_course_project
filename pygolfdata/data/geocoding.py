import pandas as pd
import requests

url = "https://maps.googleapis.com/maps/api/geocode/json"

# This is my API key attached to my own credit card
api_key = 'AIzaSyAJVeBf_Oc4ngcifbE_a_m6c1QDYBFhXlI'

PATH = './golf_course_project_data/'
courses = pd.read_csv(PATH + 'courses.txt')

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

