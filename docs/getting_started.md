# Getting started

To get started analyzing ShotLink and weather data:
- If you don't have Git LFS installed already, [install it](https://git-lfs.github.com). 
- You'll also need git and Python 3.x - we've developed with Python 3.6.
- Clone the [repo](https://github.com/awfuldynne/golf_course_project). If you have access, this will pull down the data using the private data repo, as explained in the [Data.md](data.md doc. If you don't have access, TBD what happens, specifically?
- Unzip the data (we store it compressed to save disk space and network bandwidth, since Git LFS charges for both by the byte). In the 'data' directory, run 'python unzip.py'.
- Now you can load already-prepared data by importing the shotlink module and calling get_combined_data_from_file, as shown in the [Analysis Notebook Start Example.ipynb](Analysis Notebook Start Example.ipynb) file. For example:
    import pandas as pd

    from pygolfdata.data import shotlink

    # load just the 2016 data
    d = shotlink.get_combined_data_from_file('data/combined_shots_and_weather_2016_2016.csv')


If you don't have access to the repo, you can still use the code. You'd need to retrieve the ShotLink data from the PGA Tour site yourself. The functions in the shotlink.py module take the path to the data as an argument, and assume a layout like that documented in the [data documentation](data.md).