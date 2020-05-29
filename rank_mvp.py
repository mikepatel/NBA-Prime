"""
Michael Patel
May 2020

Project description:
    Use basketball reference data to rank every MVP winner's campaign since 2000

File description:
    Use basketball reference data to rank every MVP winner's campaign since 2000
"""
################################################################################
# Imports
import os
import re
import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Pool, Queue

from constants import *


################################################################################
class Player:
    def __init__(self, record):
        self.record = record.copy()
        self.url = self.record["URL"]
        self.year = self.record["Year"]

        with urllib.request.urlopen(self.url) as response:
            page = response.read()

        page = re.sub('<!--|-->', "", str(page))

        # html soup
        self.soup = BeautifulSoup(page, "html.parser")

        # get player info
        self.name = self.get_name()
        self.row = self.get_row()
        self.points = self.get_points()
        self.rebounds = self.get_rebounds()
        self.assists = self.get_assists()
        self.team = self.get_team()
        self.team_wins = self.get_team_wins()
        self.memorability = int(self.record["Memorability"])
        self.hitp_index = self.calculate_hitp_index()

        # populate record
        self.populate_record()

    # get name
    def get_name(self):
        name = self.soup.title.text
        name, _ = name.split("Stats")
        name = name.replace("\\", "")
        name = name.strip()
        return name

    # get specific mvp row
    def get_row(self):
        row_id = "per_game." + str(self.year)
        row = self.soup.find("tr", {'id': row_id})
        return row

    # get points
    def get_points(self):
        points = self.row.find("td", {"data-stat": "pts_per_g"}).text.strip()
        points = float(points)
        return points

    # get rebounds
    def get_rebounds(self):
        rebounds = self.row.find("td", {"data-stat": "trb_per_g"}).text.strip()
        rebounds = float(rebounds)
        return rebounds

    # get assists
    def get_assists(self):
        assists = self.row.find("td", {"data-stat": "ast_per_g"}).text.strip()
        assists = float(assists)
        return assists

    # get TS%

    # get team
    def get_team(self):
        team = self.row.find("td", {"data-stat": "team_id"}).text.strip()
        return team

    # get team record (wins)
    def get_team_wins(self):
        url_wins = "https://www.basketball-reference.com/teams/" + str(self.team) + "/" + str(self.year) + ".html"

        with urllib.request.urlopen(url_wins) as response:
            page = response.read()

        page = re.sub('<!--|-->', "", str(page))

        # html soup
        wins_soup = BeautifulSoup(page, "html.parser")

        wins = wins_soup.find("td", {"data-stat": "wins"}).text.strip()
        wins = int(wins)
        return wins

    # calculate HITP index
    def calculate_hitp_index(self):
        # weights
        w_pts = 1
        w_rebs = 1
        w_asts = 1
        w_wins = 1
        w_memorability = 0

        hitp_index = np.sum([
            w_pts*self.points,
            w_rebs*self.rebounds,
            w_asts*self.assists,
            w_wins*self.team_wins,
            w_memorability*self.memorability
        ])
        return hitp_index

    # populate record
    def populate_record(self):
        self.record["Points"] = self.points
        self.record["Rebounds"] = self.rebounds
        self.record["Assists"] = self.assists
        self.record["Wins"] = self.team_wins
        self.record["HITP Index"] = self.hitp_index


################################################################################
def run(record):
    p = Player(record)
    return p.record


################################################################################
# Main
if __name__ == "__main__":
    # Read in CSV
    df = pd.read_csv(MVP_CSV)

    # pass in row, receive back populated row
    # then rank rows
    records = []
    for index, row in df.iterrows():
        records.append(row)

    processes = Pool(processes=len(records))
    data = processes.map(run, records)
    processes.close()

    # Write to CSV
    mvp_df = pd.DataFrame(data)
    mvp_df = mvp_df.sort_values(by=["HITP Index"], ascending=False)
    mvp_results_csv = os.path.join(MVP_RESULTS_DIR, "mvp_results.csv")
    mvp_df.to_csv(mvp_results_csv, index=False)
