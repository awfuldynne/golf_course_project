# WeatherDateAPI Class

### Overview
One of the goals of this package is to provide an API to manage both the PGA ShotLink data as well as to provide a means to combine that data together with historical weather data. The WeatherDateAPI class under the weather package does exactly that. By passing in a date, latitude, and longitude the WeatherDateAPI class leverages the [DarkSky API](https://darksky.net/dev) to pull historical weather data and then write the data out to disk to persist data in a CSV-file.

To simplify the work done by the WeatherDateAPI class, we take advantage of the python library [darkskylib](https://pypi.org/project/darkskylib/) to wrap our calls to DarkSky.

### Example Code
The following code is an example of how to leverage the WeatherDateAPI class. 

1. Initialize an instance with your DarkSky API Key and local file path. 
2. Make calls to append more data to the DataFrame.
	1. If the data already exists, that request will be ignored.
3. Once you're through appending data, write the DataFrame out to file.

```(python)
from datetime import date

from weather import core

w = core.WeatherDateApi("APIKEY", "PATH_TO_CSV")
w.append_weather_data(21.0068, -156.64, date(2012, 1, 6))
w.append_weather_data(34.0498, -118.5013, date(2008, 3, 14))
w.append_weather_data(29.6181278, -81.238804, date(2008, 11, 2))
w.write_dataframe_to_file()

print("Print the first 5 rows")
print(w.get_weather_dataframe().head(5))
```

### Limitations
The DarkSky API is kind enough to allow 1000 free calls to be made each day, but any calls beyond that are charged $0.0001 per call (or 100 calls per cent). The data provided by the DarkSky API is at the level of hour of the day. If a more granular level of data is needed, a different historical weather data API would need to be used.
