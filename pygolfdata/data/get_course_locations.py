"""
Obtains the latitude and longitude for each course, outputting the result to a file called
courses_geocoded.txt.
"""
import pandas as pd
import requests

import shotlink

def main():
    """Get a list of unique course names, then send a separate request for each course."""
    df = shotlink.get_shots(range(2012, 2018), 'data') # just get 2012-2017, for now at least
    courses = df['CourseName'].unique()

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    # This is my API key attached to my own credit card
    api_key = 'insert_your_own_api_key_here'

    latlong = []
    results = None

    for name in courses:
        params = {'key': api_key, 'address': name}
        print(name)
        rg = requests.get(url, params=params)
        results = rg.json()['results']
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

