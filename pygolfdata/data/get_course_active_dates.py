import shotlink

def main():
    df = shotlink.get_active_course_dates(range(2008, 2018), '../../../golf_course_project_data')
    df.to_csv('active_course_dates.csv', index=False)

if __name__ == '__main__':
    main()