# ShotLink code

## Overview

The ShotLink code enables access to a cleaned and merged set of per-stroke data. For more information about the underlying ShotLink data and files, see the [Data](data.md) doc.

In general, see the code and the docstrings in code for more in-depth information. This document just provides an overview.

## Library: shotlink.py

The shotlink.py module provides functions to access the ShotLink data, depending on whether you want to load the data from the source files provided by the PGA Tour, or to load an already-combined data set - including weather data.

To load data from the PGA Tour's ShotLink source data:
- Call 'get_shots_augmented', passing a list of the years you want to retrieve and the path to the source data. This function returns a DataFrame containing a row per stroke for the specified years. The data is 'augmented' because it contains both data from the ShotLink 'shot' and 'course level' datasets. The function loads the data using  the explicit data types listed in the SHOT_DTYPES and COURSELEVEL_DTYPES dictionaries, which vastly reduces the in-memory footprint of the data. For example:
`shots = shotlink.get_shots_augmented([2016, 2017], '../data')`
- To clean the data and apply a set of useful preparatory steps, call 'prepare_shots'. For example, this function converts date fields to datetime instances (which takes a while, so we don't do it on load), fixes an incorrect date in the source, adds a 'ShotDateAndTime' field that combines the shot date and time data, and adds a 'PlayerName' field that holds each player's full name. For example:
`shots = shotlink.prepare_shots(shots)`

To load an already processed set of data - to get a DataFrame instance with a row per shot, including weather data, call 'get_combined_data_from_file', like this:
`d = shotlink.get_combined_data_from_file('../data/combined_shots_and_weather_2012_2016.csv)`

The shotlink.py file contains additional functions. See the file for details.

## ShotLink scripts

The pygolfdata package includes a set of scripts that use shotlink.py. For further information, see the code and docstrings in the following files:
- [../pygolfdata/data/get_course_locations.py](get_course_locations.py)
- [../pygolfdata/data/get_course_active_dates.py](get_course_active_dates.py)
- [../pygolfdata/data/get_combined_weather_and_course_data.py](get_combined_weather_and_course_data.py)
- [../pygolfdata/data/get_combined_shot_and_weather_data.py](get_combined_shot_and_weather_data.py)