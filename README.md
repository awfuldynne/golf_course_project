# pygolfdata
[![Build
Status](https://travis-ci.org/awfuldynne/golf_course_project.svg?branch=master)](https://travis-ci.org/awfuldynne/golf_course_project)
[![codecov](https://codecov.io/gh/awfuldynne/golf_course_project/branch/master/graph/badge.svg)](https://codecov.io/gh/awfuldynne/golf_course_project)

Pygolfdata is a tool to help users interested in correlating [PGA ShotLink](https://www.pgatour.com/stats/shotlinkintelligence/overview.html) data with weather data. Weather observations are taken from a historical weather API that provides hourly snapshots.

# Installation

To get started analyzing ShotLink and weather data:
- If you don't have Git LFS installed already, [install it](https://git-lfs.github.com). 
- You'll also need git and Python 3.x - we've developed with Python 3.6.
- Clone the [repo](https://github.com/awfuldynne/golf_course_project). If you have access, this will pull down the data using the private data repo, as explained in the [data documentation](docs/data.md). (If you don't have access to the repo, you can still use the code. You'd need to retrieve the ShotLink data from the PGA Tour site yourself. The functions in the shotlink.py module take the path to the data as an argument, and assume a layout like that documented in the data documentation.)
- Unzip the data (we store it compressed to save disk space and network bandwidth, since Git LFS charges for both by the byte). In the 'data' directory, run 'python unzip.py'.
- You'll want to set your working directory to the `golf_course_project` folder and run the `setup.py` file.
```
cd golf_course_project
python setup.py install
```
- To ensure that you have all of the necessary packages to run `pygolfdata` locally you'll also want to install all of the requirements:
```
pip install -r requirements.txt
```
- Now you can load already-prepared data by importing the shotlink module and calling get_combined_data_from_file, as shown in the [Analysis Notebook Start Example](https://github.com/awfuldynne/golf_course_project/blob/master/Examples/Analysis%20Notebook%20Start%20Example.ipynb) notebook. For example:
```
import pandas as pd

from pygolfdata.data import shotlink

# load just the 2016 data
d = shotlink.get_combined_data_from_file('data/combined_shots_and_weather_2016_2016.csv')
```

# Data
For more information about the data, read the [data documentation](docs/data.md).

# Examples
For how to leverage the data set generated by pygolfdata, please refer to the [examples](https://github.com/awfuldynne/golf_course_project/tree/master/Examples) section of the project.

# Code
The docs directory has more information about the [ShotLink code](docs/shotlink.md) and the [weather code](docs/weather_date_api_doc.md). 

# Project Organization
TODO update with final set of files
```
golf_course_project
├ docs
│   ├ data.md
│   ├ design.md
│   ├ example_document.txt
│   ├ images
│   │   └ pga_web_scraping_example.png
│   ├ shotlink.md
│   ├ Weather Data APIs - tech review.pdf
│   └ weather_date_api_doc.md
├ Examples
│   └ Analysis and Visualization.ipynb
├ pygolfdata
│   ├ data
│   │   ├ get_combined_shot_and_weather_data.py
│   │   ├ get_combined_weather_and_course_data.py
│   │   ├ get_course_active_dates.py
│   │   ├ __init__.py
│   │   └ shotlink.py
│   ├ __init__.py
│   ├ run_tests.sh
│   ├ tests
│   │   ├ __init__.py
│   │   ├ test_shotlink_data.py
│   │   └ test_weather_module.py
│   └ weather
│       ├ core.py
│       ├ __init__.py
│       ├ test_data
│       │   └ weather_date_api_test.csv
│       └ tests
├ .coveragerc
├ .gitignore
├ .gitmodules
├ .travis.yml
├ DataSetupReadme.md
├ LICENSE
├ pylintrc
├ README.md
├ requirements.txt
├ setup.py
└ TravisDeployKey.enc
```
# Limitations
The use of PGA Shotlink data is restricted to academic purposes and requires that a user fill out the linked form to request their own access.

Access to the [Dark Sky](https://darksky.net/dev) API is gated by requesting an API key. While initially free, this API has a limit on usage per day before requiring payment.

# Acknowledgements
This library is possible in part to being Powered by [DarkSky API](https://darksky.net/poweredby/) and from the data generously offered by [PGA ShotLink](https://www.pgatour.com/stats/shotlinkintelligence/overview.html).

# Contact
Interested in reaching out to us with questions or comments? pygolfdata@googlegroups.com
