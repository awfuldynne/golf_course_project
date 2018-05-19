"""
Script that retrieves data summarizing which courses hosted tournaments on which days, for
use in retrieving weather data (because we want weather for each of these days in these locations).
"""

import shotlink

def main():
    """Get activate dates and output as csv."""
    df = shotlink.get_active_course_dates(range(2008, 2018), '../../../golf_course_project_data')
    df.to_csv('active_course_dates.csv', index=False)

if __name__ == '__main__':
    main()
