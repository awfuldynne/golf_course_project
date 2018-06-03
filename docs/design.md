# Use cases
- Data scientists can analyze PGA ShotLink data and weather data, together.
- Example research questions:
	- How does the presence of rain/wind/cloud cover affect golfer performance?
    - How does intensity of rain/wind/cloud cover affect golfer performance?
    - Which golfers are most affected by weather events?

# Use Case Examples

## Data Analysis and Predictive Modeling

###### What it does?
The analysis and modeling component of our project takes the finalized output of the ShotLink, weather, and golf course location data to look for meaningful relationships between golfer performance and weather. Initial exploratory analysis utilizing data visualization and hypothesis testing will provide guidance for the predictive modeling. Example questions to explore include:
- How does wind speed/rain/temperature affect average shots gained, if at all?
- Which golfers have the highest shots gained given certain weather conditions?

Subsequent models will look to predict shots gained (for individual golfers or as a tournament-wide aggregate) given a course and weather conditions. We'll utilize the scikit-learn package for model building and evaluation.

###### Input(s):
- (pandas DataFrame) Cleaned ShotLink data
- (pandas DataFrame) Cleaned Weather data
- (pandas DataFrame) Cleaned Course location data

###### Output(s):
- (Jupyter notebook) Exploratory analysis
        - Visualizations
        - Hypothesis tests
- (Jupyter notebook) Predictive model training, testing, and evaluation

## Visualization

###### What it does?
The visualizations provide deeper insight into the effects discovered from the model. As such, the statistical model becomes an input to the charts, graphs, plots describing the degree of the effects, differences between their amplitudes, any interactions or correlations between them.
Though these are largely derived during the data analysis and model formation, it is a feature on its own to the user.

###### Input(s):
- (scikit-learn Generalized Linear Model) Built from Shotlink and weather data

###### Output(s):
For each statistically significant effect, interaction, correlation:
- a plot showing its effect on the response variable, shots gained on the y-axis.
        - continuous predictors like "Temperature" will use a plot with a linear or logarithmic x-axis
        - discrete predictors like "Is Raining" will use a box plot, with each category on the x-axis
        - two-way interactions among variables will use contour plots, with the two on the x and y-axis, and shots gained on the contour.

# Components

## ShotLink Data

###### What it does?
Combines, cleans, and returns a single dataframe with ShotLink data, per kind of data. The ShotLink data comes from the PGA, and includes selected data per stroke, per hole, per round, and per event, as well as additional selected data per course, and for launch and trajectory data per shot via radar. The source data generally exists per year, so 'combining' refers to reading and combining multiple years. 'Cleaning' includes both things like renaming columns (the source data has column names with spaces in odd places, for example) and modifying data to make it work better with ML algorithms (like bucketing categorical variables, making missing data consistent so all missing data is represented in the same way, and so on). The code also uses pandas best practices for explicitly defining data types per field to manage the size of the data (in testing, a year's worth of shot data takes 2gb of RAM with the default settings but only 450mb when we specify data types explicitly).

###### Input(s):
- The kind of data (stroke, hole, round, event, course, radar launch, radar trajectory). Each kind of data will have it  own method (get_shots, get_holes, , etc.)
- (sequence/list) Years requested, as a sequence of integers ([2007, 2008], etc.)

###### Output(s):
- (pandas DataFrame) The requested data, with columns from the underlying ShotLink data (tour, player number, player name, hole number, etc.)
- (csv file) Comma delimited file 

###### Leveraged By:
- Geolocation
	- Requires PGA Tour course name to retrieve latitude and longitude for the course.
- Merge Weather/ShotLink Data
	- Requires ShotLink data to combine with weather data to generate the combined data set.

## Geolocation Data

###### What it does?
While the data provided by ShotLink tells us the name of the course where a given tournament was played, the DarkSky API requires that a latitude and longitude be passed in to request historical weather data. To bridge this gap we will leverage the [Google Geocoding API](https://developers.google.com/maps/documentation/geolocation/intro) to map a course name to latitude and longitude.

###### Input(s):
- (pandas DataFrame) ShotLink data

###### Output(s):
- (csv file) Comma delimited file containing the course name, latitude, longitude and address

###### Leveraged By
- Weather Data
	- Requires the latitude and longitude of courses.

## PGA Tour Event Data

###### What it does?
For the weather data component to be able to retrieve data it needs both geolocation data and when a tournament was played at a given location. From the ShotLink data, we'll generate a file containing a distinct list of dates where a tournament was played on a given course.

###### Input(s):
- (pandas DataFrame) ShotLink data

###### Output(s):
- (csv file) Comma delimited file containing the course name and event date

###### Leveraged By
- Weather Data
	- Requires the date a PGA Tour event occurred on for a given course.

## Weather Data

###### What it does?
The weather data component of our analysis retrieves, cleans, and archives historical weather conditions for the duration of a given PGA tournament. Leveraging [DarkSky's](https://darksky.net/dev) weather API we can pass in a latitude, longitude, and date to retrieve hourly weather conditions for that day. To simplify the API call we leverage the python package [darkskylib](https://pypi.org/project/darkskylib/0.2.4/). After retrieving the data, the component will clean the JSON response into pandas DataFrame containing columns of data that correspond to weather measurements such as cloud cover, wind speed, and temperature. Once the data is cleaned, the data will be appended to a DataFrame that is archived off as a csv file so that future requests of the same latitude, longitude, and date can first check to see if the data already exists.

#### Retrieval

###### Input(s):
- (String) DarkSky API Key
- (Float) Latitude
- (Float) Longitude
- (Date) Date

###### Output(s):
- (String) JSON Response from the DarkSky API

#### Cleaning

###### Input(s):
- (String) JSON Response from the DarkSky API

###### Output(s):
- (pandas DataFrame) DataFrame containing weather data in a form like ['utc_date', 'hour', 'temperature (Fahrenheit)', 'rain', 'wind_speed_mph', 'wind_direction']

#### Archiving

###### Input(s):
- (pandas DataFrame) DataFrame containing weather data

###### Output(s):
- (pandas DataFrame) DataFrame containing an updated archive of weather data
- (csv file) Comma delimited file containing an archive of weather data

###### Leveraged By:
- Merge Weather/ShotLink Data
	- Requires weather data to combine with ShotLink data to generate the combined data set.

#### Limitations
One of the limitations of this API is that to query the historical weather data a user requires an API key. The base API key is limited to only 1000 requests per day. After 1000 requests have been made, additional requests can be made at the cost of $1/10,000 requests.

## Merge Weather/ShotLink Data

###### What it does?
To generate the final output data set, the pygolfdata library takes the data provided by the ShotLink component and the data provided by the weather component and maps a shot and the hour that shot was taken to the corresponding record in the weather data set. After the data has been combined it is written out to csv and that csv file is archived in a zip. Both the csv and zip archive are then moved to the root data directory.

###### Input(s):
- (pandas DataFrame) ShotLink data
- (pandas DataFrame) Weather data

###### Output(s):
- (pandas DataFrame) DataFrame containing shot level data alongside weather measurements for the hour the shot was taken
- (csv file) Comma delimited file containing shot level data alongside weather measurements for the hour the shot was taken
- (zip archive) Zip archive containing the above csv file

###### Leveraged By
- Example Use Cases
	- Requires the cleaned output data set to perform analyses

