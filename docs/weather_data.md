# Weather Data

### Overview
Part of the goal of this analysis is to understand how the metric ShotsGained behaves depending on the weather at the time of the shot. Unfortunately, the PGA ShotLink dataset doesn't provide granular weather details so we must look to retrieve a historical snapshot for each of the tournaments we have weather on.

[WeatherUnderground](https://www.wunderground.com/weather/api/) provides an API from which you can query historical weather data and while it is tempting to leverage this API into exactly what we need, the python package [WunderWeather](https://pypi.org/project/WunderWeather/1.0.0/) handles the functionality that we require. To leverage WeatherWunder, it still requires an API key to be requested from WeatherUnderground.

### Examples
###### Seattle, WA - 09/30/1987

```(python)
from pprint import pprint
import arrow
from WunderWeather import weather

# setup
api_key = "API KEY"
location = 'WA/Seattle'
extractor = weather.Extract(api_key)

# Get data
date = arrow.get("19870930", "YYYYMMDD")
response = extractor.date(location, date.format('YYYYMMDD'))
pprint(response.data)
```
###### Example Output

```
{'conds': 'Clear',
   'date': {'hour': '07',
			'mday': '30',
			'min': '00',
			'mon': '09',
			'pretty': '7:00 AM PDT on September 30, 1987',
			'tzname': 'America/Los_Angeles',
			'year': '1987'},
   'dewpti': '48.0',
   'dewptm': '8.9',
   'fog': '0',
   'hail': '0',
   'heatindexi': '-9999',
   'heatindexm': '-9999',
   'hum': '89',
   'icon': 'clear',
   'metar': 'METAR KBFI 301400Z 13003KT 10SM CLR 11/09 A3012 '
			'RMK SLPNO T01060089',
   'precipi': '-9999.00',
   'precipm': '-9999.00',
   'pressurei': '30.12',
   'pressurem': '1019.9',
   'rain': '0',
   'snow': '0',
   'tempi': '51.1',
   'tempm': '10.6',
   'thunder': '0',
   'tornado': '0',
   'utcdate': {'hour': '14',
			   'mday': '30',
			   'min': '00',
			   'mon': '09',
			   'pretty': '2:00 PM GMT on September 30, 1987',
			   'tzname': 'UTC',
			   'year': '1987'},
   'visi': '10.0',
   'vism': '16.1',
   'wdird': '130',
   'wdire': 'SE',
   'wgusti': '-9999.0',
   'wgustm': '-9999.0',
   'windchilli': '-999',
   'windchillm': '-999',
   'wspdi': '3.5',
   'wspdm': '5.6'},
```
