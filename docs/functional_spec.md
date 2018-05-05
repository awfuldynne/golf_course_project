# Use cases
- Data scientists can analyze PGA ShotLink data and weather data, together.
- Example research questions:
	- How does the presence of rain/wind/cloud cover affect golfer performance? 
	- How does intensity of rain/wind/cloud cover affect golfer performance?
	- Which golfers are most affected by weather events?

# Components

## ShotLink data

###### What it does?
Combines, cleans, and returns a single dataframe with ShotLink data, per kind of data. The ShotLink data comes from the PGA, and includes selected data per stroke, per hole, per round, and per event, as well as additional selected data per course, and for launch and trajectory data per shot via radar. The source data generally exists per year, so 'combining' refers to reading and combining multiple years. 'Cleaning' includes both things like renaming columns (the source data has column names with spaces in odd places, for example) and modifying data to make it work better with ML algorithms (like bucketing categorical variables, making missing data consistent so all missing data is represented in the same way, and so on). The code also uses pandas best practices for explicitly defining data types per field to manage the size of the data (in testing, a year's worth of shot data takes 2gb of RAM with the default settings but only 450mb when we specify data types explicitly).

###### Input(s):
- The kind of data (stroke, hole, round, event, course, radar launch, radar trajectory). Each kind of data will have it  own method (get_shots, get_holes, , etc.).
- (sequence/list) Years requested, as a sequence of integers ([2007, 2008], etc.).

###### Output(s):
- (pandas DataFrame) The requested data, with columns from the underlying ShotLink data (tour, player number, player name, hole number, etc.).

## Weather Data

###### What it does?
The weather data component of our analysis retrieves, cleans, and archives historical weather conditions for the duration of a given PGA tournament. Leveraging [WeatherUnderground's](https://www.wunderground.com/weather/api/) weather API we can pass in a city, state, and date and retrieve hourly weather conditions for that day. To simplify the API call we leverage the python package [WunderWeather](https://pypi.org/project/WunderWeather/1.0.0/). After retrieving the data, the component will clean the JSON response into pandas DataFrame containing columns of data that correspond to weather measurements such as cloud cover, wind speed, and temperature. Once the data is cleaned, the DataFrame will be appended to a DataFrame that is archived off as a csv file so that future requests of city, state, and date can first check to see if the data already exists.

#### Retrieval

###### Input(s):
- (String) WeatherUnderground API Key
- (String) City
- (String) State
- (Date) Start Date
- (Date) End Date

###### Output(s):
- (String) JSON Response from the WeatherUnderground API

#### Cleaning

###### Input(s):
- (String) JSON Response from the WeatherUnderground API

###### Output(s):
- (pandas DataFrame) DataFrame containing weather data in a form like ['utc_date', 'hour', 'temperature (Fahrenheit)', 'rain', 'wind_speed_mph', 'wind_direction']

#### Archiving

###### Input(s):
- (pandas DataFrame) DataFrame containing weather data

###### Output(s):
- (pandas DataFrame) DataFrame containing an updated archive of weather data
- (csv file) Comma delimited file containing an archive of weather data

#### Limitations
One of the limitations of this API is that to query the historical weather data a user requires an API key. The base API key is limited to only 10 requests per minute and 500 requests per week. This can limit the amount of new data that can be processed and archived.

## Data Analysis and Predictive Modeling

###### What it does?
The analysis and modeling component of our project joins the outputs of the ShotLink, weather, and golf course location data to look for meaningful relationships between golfer performance and weather. Initial exploratory analysis utilizing data visualization and hypothesis testing will provide guidance for the predictive modeling. Example questions to explore include:
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


## ShotLink data - Weather data Connector

###### What it does?

There is a gap between ShotLink data, which provides the name of the tournament, and Weather Underground data, which requires the city and the state of where the tournament takes place. Unfortunately there is no dataset publicly available to bridge this gap. The only viable option is to scrape PGA Tournament Schedule website for this kind of information. We decided to use BeautifulSoup (BS) Python package to do this job because of its reliability and ease of use. Please see attached [pga_web_scraping_example.png](https://github.com/awfuldynne/golf_course_project/blob/master/docs/images/pga_web_scraping_example.png) as an example screenshot of PGA Tournament website and its HTML elements.

###### Input(s):
- (pandas DataFrame) ShotLink data
- (HTML) PGA Tournament Schedule website

###### Output(s):
- (pandas DataFrame) City & State data appended to ShotLink data 

###### Package(s):
- pandas
- BeautifulSoup

## Visualization

###### What it does?

The visualizations provide deeper insight into the effects discovered from the model. As such, the statistical model becomes an input to the charts, graphs, plots describing the degree of the effects, differences between their amplitudes, any interactions or correlations between them. 
Though these are largely derived during the data analysis and model formation, it is a feature on its own to the user. 

###### Input(s):
- (scikit-learn Generalized Linear Model) Built from Shotlink and weather data. 

###### Output(s):
For each statistically significant effect, interaction, correlation:
- a plot showing its effect on the response variable, shots gained on the y-axis.
	- continuous predictors like "Temperature" will use a plot with a linear or logarithmic x-axis
	- discrete predictors like "Is Raining" will use a box plot, with each category on the x-axis
	- two-way interactions among variables will use contour plots, with the two on the x and y-axis, and shots gained on the contour. 
