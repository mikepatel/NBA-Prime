"""
Michael Patel
May 2020

Project description:
    Use basketball reference data to rank every MVP winner's campaign since 2000

File description:
    To get basketball reference data
"""
################################################################################
# Imports
import os
import re
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

from constants import *


################################################################################
class Player:
    def __init__(self, url, year):
        self.url = url
        self.year = year
        with urllib.request.urlopen(self.url) as response:
            page = response.read()

        page = re.sub('<!--|-->', "", str(page))

        # html soup
        self.soup = BeautifulSoup(page, "html.parser")

        # get player info
        self.name = self.get_name()
        self.row = self.get_row()
        self.points = self.get_points()

    # get name
    def get_name(self):
        name = self.soup.title.text
        name, _ = name.split("Stats")
        name = name.replace("\\", "")
        name = name.strip()
        return name

    # get specific mvp row
    def get_row(self):
        xpath = '//*[@id="per_game.' + str(self.year) + '"]'
        x = "per_game." + str(self.year)
        row = self.soup.find("tr", {'id': x})
        return row

    # get points
    def get_points(self):
        points = self.row.find("td", {'data-stat': 'pts_per_g'}).text.strip()
        return points


################################################################################
# Main
if __name__ == "__main__":
    # Read in CSV
    df = pd.read_csv(MVP_CSV)

    years = df["Year"]
    urls = df["URL"]

    p = Player(urls[0], years[0])
    print(p.name)
    print(p.points)

    # Write to CSV
