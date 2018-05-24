#! /usr/bin/env python
# Setup modulde for pygolfdata
#
# License: MIT


from setuptools import setup, find_packages
PACKAGES = find_packages()


OPTS = dict(
    name='pygolfdata',
    maintainer='Sean Miller',
    maintainer_email='millsea0@uw.edu',
    description='PGA Shotlink data + Weather data library',
    long_description=('pygolfdata - Accident-Weather Analysis Tool for data'
                      ' scraping, cleaning, merging and analysis'),
    url='https://github.com/awfuldynne/golf_course_project',
    license='MIT',
    author='pygolfdata',
    version='0.1',
    packages=PACKAGES,
    package_data={'pygolfdata':
                      ['data/*',
                       'tests/*',
                       'weather/*']},
    )

if __name__ == '__main__':
    setup(**OPTS)
