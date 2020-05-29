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
    def __init__(self, url):
        self.url = url
        with urllib.request.urlopen(self.url) as response:
            page = response.read()

        page = re.sub('<!--|-->', "", str(page))

        # html soup
        self.soup = BeautifulSoup(page, "html.parser")

        # get player name
        self.name = self.get_name()

    # get name
    def get_name(self):
        name = self.soup.title.text
        name, _ = name.split("Stats")
        name = name.replace("\\", "")
        name = name.strip()
        return name


################################################################################
# Main
if __name__ == "__main__":
    # Read in CSV
    df = pd.read_csv(MVP_CSV)

    url_list = df["URL"]
    url = url_list[0]

    p = Player(url)
    print(p.name)

    # Write to CSV
