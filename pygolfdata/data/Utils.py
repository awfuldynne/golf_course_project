from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
import requests
import re

# global variables
TOURNAMENT_URL = 'https://www.pgatour.com/tournaments/schedule.history.{}.html'
COL_NAMES = ['Tournament Name', 'Course Name', 'City', 'State']


def read_tour_page(url=TOURNAMENT_URL, tournament_list):
    r = requests.get(url)
    if r.status_code == 200:
        tournament_html = r.text
        soup = BeautifulSoup(r.text, 'html.parser')
        tournament_info = soup.find_all("div", class_="tournament-text")
        if len(tournament_info) == 0:
            print('Fail to scarpe tournament info from {}'.format(url))
            return None
        location_df = pd.DataFrame(columns=['Tournament Name','Location'])
        for x in tournament_list:
            for y in tournament_info:
                tour = y.get_text().lower()
                if x.lower() in tour:
                    p = re.compile(',\\xa0([a-z]+)')
                    loc = ', '.join(p.findall(tour))
                    location_df.append({x:loc}, ignore_index=True)
                    continue
    return location_df


def get_tournament_info(shot_df):
    # tournament_df = pd.DataFrame(columns=COL_NAMES)
    tournaments = shot_df['Tournament Name'].str.lower().unique()
    return tournaments

# def main():


# if __name__ == "__main__":
#     main()