# Use cases
- Data scientists can analyze PGA ShotLink data and weather data, together.

# Components

## Shotlink data
- What it does: Combines, cleans, and returns a single dataframe with ShotLink data, per kind of data. The ShotLink data comes from the PGA, and includes selected data per stroke, per hole, per round, and per event, as well as additional selected data per course, and for launch and trajectory data per shot via radar. The source data generally exists per year, so 'combining' refers to reading and combining multiple years. 'Cleaning' includes both things like renaming columns (the source data has column names with spaces in odd places, for example) and modifying data to make it work better with ML algorithms (like bucketing categorical variables, making missing data consistent so all missing data is represented in the same way, and so on). The code also uses pandas best practices for explicitly defining data types per field to manage the size of the data (in testing, a year's worth of shot data takes 2gb of RAM with the default settings but only 450mb when we specify data types explicitly). 
- Inputs: 
  - The kind of data (stroke, hole, round, event, course, radar launch, radar trajectory. I'll likely do this as separate methods (get_shotlink_strokes, etc.).
  - Years requested, as a Python sequence of integers ([2007, 2008], etc.).
- Outputs:
  - pandas DataFrame with the requested data.

## weather, retrieval/cleaning/prep
## golf course -> city/state
## model/analysis - GLM using table w/ columns built from Shotlink, weather data
## data product - for example, one+ Jupyter notebooks
## visualization?
