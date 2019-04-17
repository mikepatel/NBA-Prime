"""
Michael Patel
March 2019

version: Python 3.6.5

File Description:

Notes:
    - BeautifulSoup4
    - Basketball Reference
    - printout in table format
    - use 'm_value' statistic for each season
        - 'm_value' is constructed from a weighted combination of several statistics such as:
            - points, rebounds, assists
            - PER, true shooting, FT shooting

"""

################################################################################
# IMPORTs
from bs4 import BeautifulSoup
import urllib  # standard library
import csv
import os
import numpy as np
from prettytable import PrettyTable
import re


################################################################################
# website to crawl
url = "https://www.basketball-reference.com/players/j/jamesle01.html"  # LeBron James
#url = "https://www.basketball-reference.com/players/b/bryanko01.html"  # Kobe Bryant
#url = "https://www.basketball-reference.com/players/d/duranke01.html"  # Kevin Durant
#url = "https://www.basketball-reference.com/players/h/hardeja01.html"  # James Harden
#url = "https://www.basketball-reference.com/players/c/curryst01.html"  # Steph Curry
#url = "https://www.basketball-reference.com/players/w/wadedw01.html"  # Dwayne Wade
#url = "https://www.basketball-reference.com/players/n/nowitdi01.html"  # Dirk Nowitzki


with urllib.request.urlopen(url) as response:
    page = response.read()

soup = BeautifulSoup(re.sub("<!--|-->", "", str(page)), "html.parser")
print("\n------------------------------------------------------------------------")


# function that returns NBA player's name from Basketball Reference page
def get_player_name():
    name = soup.title.text.strip()
    name, _ = name.split("Stats")
    name = name.strip()
    #print(name)
    return name


class Player:
    def __init__(self):
        self.CAREER_STATS_REG = {}  # Regular Season
        self.CAREER_STATS_PLAYOFFS = {}  # Playoffs

        self.SEASONS = []  # year xxxx-xx
        self.AGE = []  # age at start of season
        self.TEAM = []  # NBA team

        # Traditional
        self.PPG = []  # points per
        self.RPG = []  # rebounds per
        self.APG = []  # assists per
        self.STEALS = []  # steals per
        self.BLOCKS = []  # blocks per
        self.TURNOVERS = []  # turnovers per
        self.FG_PERCENT = []  # FG% per
        self.FG_3_PERCENT = []  # 3FG% per
        self.FT_PERCENT = []  # FT% per
        self.FTA = []  # free throw attempts per
        self.MPG = []  # minutes per
        self.EFF_FG = []  # effective FG% per

        # Advanced
        self.TS = []  # true shooting % per
        self.USAGE = []  # usage % per
        self.PER = []  # player efficiency rating per

        self.M_VALUE = []  # custom 'm_value' statistic

    #
    def get_prime(self, stats, stat_cat, window_size):
        avg_value = 0.0
        idx = 0

        stat_list = stats[stat_cat]

        for i in range(len(stat_list)+1-window_size):
            avg_candidate = np.mean(stat_list[i: i+window_size])

            if avg_candidate > avg_value:
                avg_value = avg_candidate
                idx = i

        seasons = self.SEASONS[idx: idx+window_size]
        ages = self.AGE[idx: idx+window_size]
        teams = self.TEAM[idx: idx+window_size]
        value_per_year = stat_list[idx: idx+window_size]

        return seasons, ages, teams, avg_value, value_per_year

    #
    def read_table_stat(self, row, feature):
        x = float(row.find("td", {"data-stat": feature}).text.strip())
        return x

    # REGULAR SEASON
    def get_reg(self, stat, window_size):
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

                # age
                age = row.find("td", {"data-stat": "age"}).text.strip()  # int, not float

                # NBA team
                team = row.find("td", {"data-stat": "team_id"}).text.strip()  # str, not float

                # find ppg feature (points)
                ppg = self.read_table_stat(row, "pts_per_g")

                # find rpg feature (rebounds)
                rpg = self.read_table_stat(row, "trb_per_g")

                # find apg feature (assists)
                apg = self.read_table_stat(row, "ast_per_g")

                # steals
                steals = self.read_table_stat(row, "stl_per_g")

                # blocks
                blocks = self.read_table_stat(row, "blk_per_g")

                # turnovers
                turnovers = self.read_table_stat(row, "tov_per_g")

                # FG %
                fg_pct = self.read_table_stat(row, "fg_pct")

                # 3pt %
                fg_3_pct = self.read_table_stat(row, "fg3_pct")

                # free throws %
                ft_pct = self.read_table_stat(row, "ft_pct")

                # free throws attempted
                ft_att = self.read_table_stat(row, "fta_per_g")

                # minutes per game
                mpg = self.read_table_stat(row, "mp_per_g")

                # effective FG %
                eFG = self.read_table_stat(row, "efg_pct")

                #
                self.SEASONS.append(season)
                self.AGE.append(age)
                self.TEAM.append(team)

                self.PPG.append(ppg)
                self.RPG.append(rpg)
                self.APG.append(apg)
                self.STEALS.append(steals)
                self.BLOCKS.append(blocks)
                self.TURNOVERS.append(turnovers)
                self.FG_PERCENT.append(fg_pct)
                self.FG_3_PERCENT.append(fg_3_pct)
                self.FT_PERCENT.append(ft_pct)
                self.FTA.append(ft_att)
                self.MPG.append(mpg)
                self.EFF_FG.append(eFG)

            except AttributeError:
                continue

        self.CAREER_STATS_REG["season"] = self.SEASONS
        self.CAREER_STATS_REG["age"] = self.AGE
        self.CAREER_STATS_REG["team"] = self.TEAM

        self.CAREER_STATS_REG["ppg"] = self.PPG
        self.CAREER_STATS_REG["rpg"] = self.RPG
        self.CAREER_STATS_REG["apg"] = self.APG
        self.CAREER_STATS_REG["steals"] = self.STEALS
        self.CAREER_STATS_REG["blocks"] = self.BLOCKS
        self.CAREER_STATS_REG["turnovers"] = self.TURNOVERS
        self.CAREER_STATS_REG["fg_pct"] = self.FG_PERCENT
        self.CAREER_STATS_REG["fg_3_pct"] = self.FG_3_PERCENT
        self.CAREER_STATS_REG["ft_pct"] = self.FT_PERCENT
        self.CAREER_STATS_REG["ft_att"] = self.FTA
        self.CAREER_STATS_REG["mpg"] = self.MPG
        self.CAREER_STATS_REG["efg_pct"] = self.EFF_FG

        # Advanced
        table = soup.find("table", id="advanced")  # find() = find a specific vs find_all()
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")

        for row in rows:
            try:
                # TS % per geame
                ts = self.read_table_stat(row, "ts_pct")

                # Usage % per game
                usage = self.read_table_stat(row, "usg_pct")

                # PER per game
                per = self.read_table_stat(row, "per")

                #
                self.TS.append(ts)
                self.USAGE.append(usage)
                self.PER.append(per)

            except AttributeError:
                continue

        self.CAREER_STATS_REG["ts_pct"] = self.TS
        self.CAREER_STATS_REG["usage_pct"] = self.USAGE
        self.CAREER_STATS_REG["per"] = self.PER

        seasons, ages, teams, avg_value, values = self.get_prime(self.CAREER_STATS_REG, stat, window_size)
        return seasons, ages, teams, avg_value, values

    # PLAYOFFS
    def get_playoffs(self):
        print("\nTO DO: playoffs")


SLIDE_WINDOW_SIZE = 3
player_name = get_player_name()
print(player_name + "'s " + str(SLIDE_WINDOW_SIZE) + " year prime by stat category:")
STATS = [
    {"Points Per Game": "ppg"},
    {"Rebounds Per Game": "rpg"},
    {"Assists Per Game": "apg"},
    {"Steals Per Game": "steals"},
    {"Blocks Per Game": "blocks"},
    {"Turnovers Per Game": "turnovers"},
    {"Field Goal % Per Game": "fg_pct"},
    {"3-Point Field Goal % Per Game": "fg_3_pct"},
    {"Free Throw % Per Game": "ft_pct"},
    {"Free Throw Attempts Per Game": "ft_att"},
    {"Minutes Per Game": "mpg"},
    {"Effective Field Goal % Per Game": "efg_pct"},
    {"True Shooting % Per Game": "ts_pct"},
    {"Usage % Per Game": "usage_pct"},
    {"PER Per Game": "per"}
    ]
p = Player()
for i in range(len(STATS)):
    stat = STATS[i]
    stat_name = list(stat.keys())[0]
    stat_abbr = list(stat.values())[0]

    years, ages, teams, _, values = p.get_reg(stat_abbr, SLIDE_WINDOW_SIZE)

    print("\n")
    table = PrettyTable()
    table.field_names = ["Years", "Age", "Team", stat_name]
    for j in range(len(years)):
        table.add_row([years[j], ages[j], teams[j], values[j]])
    print(table)



#STAT = "ppg"
#p = Player()
#years, stat_value, t = p.get_prime(STAT, SLIDE_WINDOW_SIZE)
#print(years)
#print(t)
#years = ", ".join(years)
#print("\n{} year prime for {}: {}".format(SLIDE_WINDOW_SIZE, STAT.upper(), years))
#print("{}: {:.4f}".format(STAT.upper(), stat_value))
#print("\n------------------------------------------------------------------------")

#table = PrettyTable()
#table.field_names = ["Years", STAT]
#for r in range(len(t)):
#    table.add_row([years[r], t[r]])
#print(table)