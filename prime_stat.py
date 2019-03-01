# NOTES:
#   - Python 3.6.5
#   - BeautifulSoup4
#

################################################################################
# IMPORTs
from bs4 import BeautifulSoup
import urllib  # standard library
import csv
import os
import numpy as np

################################################################################
# website to crawl
#url = "https://www.basketball-reference.com/"
url = "https://www.basketball-reference.com/players/j/jamesle01.html"
#url = "https://www.basketball-reference.com/players/j/jordami01.html"

with urllib.request.urlopen(url) as response:
    data = response.read()


################################################################################




soup = BeautifulSoup(data, "html.parser")
print("\n------------------------------------------------------------------------")
player_name = soup.title.text.strip()
player_name, _ = player_name.split("Stats")
player_name = player_name.strip()
print(player_name)
#
class Player:
    def __init__(self):
        self.CAREER_STATS_REG = {}
        self.CAREER_STATS_PLAYOFFS = {}

        # stat categories
        self.SEASONS = []
        self.PPG = []
        self.APG = []
        self.RPG = []

        # find "Per Game" table => Regular Season
        table = soup.find("table", id="per_game")  # find() = find a specific vs find_all()
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")

        for row in rows:
            try:
                # find season feature, season feature acts as dictionary key
                season = row.find("th", {"data-stat": "season"})
                season = season.a  # get URL
                season = season.text.strip()

                # find ppg feature (points)
                ppg = float(row.find("td", {"data-stat": "pts_per_g"}).text.strip())

                # find rpg feature (rebounds)
                rpg = float(row.find("td", {"data-stat": "trb_per_g"}).text.strip())

                # find apg feature (assists)
                apg = float(row.find("td", {"data-stat": "ast_per_g"}).text.strip())

                self.SEASONS.append(season)
                self.PPG.append(ppg)
                self.RPG.append(rpg)
                self.APG.append(apg)

            except AttributeError:
                continue

        self.CAREER_STATS_REG["season"] = self.SEASONS
        self.CAREER_STATS_REG["ppg"] = self.PPG
        self.CAREER_STATS_REG["rpg"] = self.RPG
        self.CAREER_STATS_REG["apg"] = self.APG

    def get_prime(self, stat, window_size):
        value = 0.0
        idx = 0

        for i in range(len(self.CAREER_STATS_REG[stat])+1-window_size):
            avg = np.mean(self.CAREER_STATS_REG[stat][i: i+window_size])

            if avg > value:
                value = avg
                idx = i

        seasons = self.SEASONS[idx: idx+window_size]

        return seasons, value


SLIDE_WINDOW_SIZE = 3
STAT = "ppg"
p = Player()
years, stat_value = p.get_prime(STAT, SLIDE_WINDOW_SIZE)
years = ", ".join(years)
print("\n{} prime years: {}".format(SLIDE_WINDOW_SIZE, years))
print("{}: {:.4f}\n".format(STAT.upper(), stat_value))


################################################################################
players_file = os.path.join(os.getcwd(), "players list.csv")
#print(players_file)

Players = {}

with open(players_file, newline="") as f:
    csv_reader = csv.reader(f, delimiter=",")

    line_count = 0
    name_key = ""
    for row in csv_reader:  # each row is a list of String elements
        if line_count == 0:  # column names
            name_key = row[0]
            line_count += 1  # skip row of column names
        else:
            name = str(row[0]).lower()  # player names lowercase
            Players[name] = {name_key: name}
            line_count += 1

#print(Players)

#for player in Players:
#    print(Players[player])  # contents of dictionary item








