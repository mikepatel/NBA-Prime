"""
Michael Patel
May 2019

version: Python 3.6.5

File Description:

Notes:
    - use pandas dataframe for holding stats

"""


################################################################################
# Imports
import os
import re
import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import matplotlib.pyplot as plt

from constants import *


################################################################################
class Player:
    def __init__(self, url):
        self.url = url
        with urllib.request.urlopen(self.url) as response:
            page = response.read()

        # html soup
        self.soup = BeautifulSoup(re.sub('<!--|-->', "", str(page)), "html.parser")

        # player name
        self.name = self.get_name()

        # bio info
        self.SEASONS = []  # year xxxx-xx
        self.AGE = []  # age at start of season
        self.TEAM = []  # NBA team

        # stats of interest
        self.PPG = []  # points per
        self.RPG = []  # rebounds per
        self.APG = []  # assists per
        self.FT_PERCENT = []  # free throw percentage per
        self.EFG_PERCENT = []  # effective field goal percentage per
        self.PER = []  # player efficiency rating per
        self.TS = []  # true shooting percentage per

        # custom statistic
        # calculated for each season
        self.M_VALUE = []

        # build dict for stat categories
        self.CATEGORIES = {
            "Season": self.SEASONS,  # season
            "Age": self.AGE,  # age
            "Team": self.TEAM,  # team
            "Points": self.PPG,  # points
            "Rebounds": self.RPG,  # rebounds
            "Assists": self.APG,  # assists
            "FT%": self.FT_PERCENT,  # FT%
            "eFG%": self.EFG_PERCENT,  # eFG%
            "PER": self.PER,  # PER
            "TS%": self.TS,  # TS%
            "M_VALUE": self.M_VALUE  # m value
        }

        # stats dataframe
        self.raw_stats_df = pd.DataFrame()

    # returns player's name
    def get_name(self):
        name = self.soup.title.text.strip()
        name, _ = name.split("Stats")
        name = name.strip()
        return name

    # update raw_stats_df (raw table)
    def update_raw_stats_df(self):
        self.raw_stats_df = pd.DataFrame({k: pd.Series(v) for k, v in self.CATEGORIES.items()})
        print(self.raw_stats_df)

    # !! CONCERNED WITH JUST REGULAR SEASON !!
    # parse html data for stats
    def get_stats(self):
        self.get_reg_season_stats()  # regular season
        self.update_raw_stats_df()

        # self.get_playoff_stats()  # playoffs

    # all regular season stats
    def get_reg_season_stats(self):
        self.get_reg_season_trad_stats()  # Regular Season: seasons, age, team,
        # points, rebounds, assists, FT%, eFG%
        self.get_reg_season_advanced_stats()  # Regular Season: PER, TS%

    # all playoff stats
    def get_playoff_stats(self):
        print("To do")
        return self

    #
    def get_reg_season_trad_stats(self):
        # Seasons, Ages, Teams, Points, Rebounds, Assists, FT %, eFG %
        rows = self.get_trad_table()

        for row in rows:
            try:
                # find season feature, season feature acts as dict key
                season = row.find("th", {"data-stat": "season"})
                season = season.a  # get URL
                season = season.text.strip()

                # age
                age = row.find("td", {"data-stat": "age"}).text.strip()  # int, not float

                # team
                team = row.find("td", {"data-stat": "team_id"}).text.strip()  # str, not float

                # points
                ppg = self.read_stat_from_table(row, "pts_per_g")
                # print("Points: ", ppg)

                # rebounds
                rpg = self.read_stat_from_table(row, "trb_per_g")
                # print("Rebounds: ", rpg)

                # assists
                apg = self.read_stat_from_table(row, "ast_per_g")
                # print("Assists: ", apg)

                # FT%
                ft_pct = self.read_stat_from_table(row, "ft_pct")
                # print("FT%: ", ft_pct)

                # eFG%
                efg_pct = self.read_stat_from_table(row, "efg_pct")
                # print("eFG%: ", efg_pct)

                # update player's bio information
                self.SEASONS.append(season)
                self.AGE.append(age)
                self.TEAM.append(team)

                # update player's traditional stats
                self.CATEGORIES["Points"].append(ppg)
                self.CATEGORIES["Rebounds"].append(rpg)
                self.CATEGORIES["Assists"].append(apg)
                self.CATEGORIES["FT%"].append(ft_pct)
                self.CATEGORIES["eFG%"].append(efg_pct)

            except AttributeError as e:
                if "attribute 'a'" in str(e):  # 'Season' is not a hyperlink
                    continue

    #
    def get_reg_season_advanced_stats(self):
        # PER, TS%
        rows = self.get_advanced_table()
        for row in rows:
            try:
                # PER
                per = self.read_stat_from_table(row, "per")
                # print("PER: ", per)

                # TS
                ts = self.read_stat_from_table(row, "ts_pct")
                # print("TS: ", ts)

                # update player's advanced stats
                self.CATEGORIES["PER"].append(per)
                self.CATEGORIES["TS%"].append(ts)

            except AttributeError:
                continue  # for now

    # "Per Game" table => Regular Season
    # 'Traditional' Stats
    def get_trad_table(self):
        # find "Per Game" table => Regular Season
        # 'Traditional' stats
        table = self.soup.find("table", {"id": "per_game"})
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        return rows

    # find "Advanced" table
    # 'Advanced' stats
    def get_advanced_table(self):
        table = self.soup.find("table", {"id": "advanced"})
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        return rows

    # returns specified column of values
    @staticmethod
    def _get_column(matrix, c_idx):
        return [row[c_idx] for row in matrix]

    # reads a particular stat value from html data
    @staticmethod
    def read_stat_from_table(row, feature):
        try:
            x = float(row.find("td", {"data-stat": feature}).text.strip())
            return x
        except AttributeError as e:
            if "attribute 'text'" in str(e):
                return float(0.0)















    # Calculates 'm_value' per player season
    def calculate_m_value(self):
        # normalize stats
        for key in self.CATEGORIES:
            self.CATEGORIES[key] = self.normalize(self.CATEGORIES[key])

        # weight values
        w1 = 0.1  # points
        w2 = 0.1  # rebounds
        w3 = 0.1  # assists
        w4 = 0.1  # FT percentage
        w5 = 0.1  # eFG percentage
        w6 = 0.1  # PER
        w7 = 0.1  # TS

        for i in range(len(self.SEASONS)):
            m_value = np.sum([
                w1*self.PPG[i][1],
                w2*self.RPG[i][1],
                w3*self.APG[i][1],
                w4*self.FT_PERCENT[i][1],
                w7 * self.EFG_PERCENT[i][1],
                w5*self.PER[i][1],
                w6*self.TS[i][1]
            ])
            m_value = np.round(m_value, decimals=4)
            self.M_VALUE.append(m_value)

    # normalize
    @staticmethod
    def normalize(stat):
        stat_min = np.min(stat)
        stat_max = np.max(stat)
        den = stat_max - stat_min

        if den == 0.0:  # Should not divide by zero
            for i in range(len(stat)):
                stat[i].append(0.0)
            return stat

        else:
            # normalize a stat value and append,
            # producing [raw_stat, normalized_stat]
            for i in range(len(stat)):
                num = stat[i][0] - stat_min
                x = num / den
                x = np.round(x, decimals=4)
                stat[i].append(x)

            return stat

    # Finds starting index for stats values list for a player's '?-year prime'
    # Use m_values for calculating prime windows
    def get_prime(self, window_size):
        avg_m_value = 0.0
        idx = 0

        for i in range(len(self.M_VALUE)+1-window_size):
            temp_variance = np.var(self.M_VALUE[i: i+window_size])
            # print(i, temp_variance)

            if temp_variance < 0.0015:  # 0.0015
                avg_candidate = np.mean(self.M_VALUE[i: i+window_size])

                if avg_candidate > avg_m_value:
                    avg_m_value = avg_candidate
                    idx = i

        return idx  # return just the index

    # Field names for PrettyTable output
    @staticmethod
    def get_table_field_names():
        return [
            "Year", "Age", "Team", "Points", "Rebounds",
            "Assists", "FT%", "eFG%", "PER", "TS%", "M_VALUE"
        ]

    # Raw stats table
    def build_raw_table(self):
        raw_table = PrettyTable()
        raw_table.field_names = self.get_table_field_names()

        for i in range(len(self.SEASONS)):
            raw_table.add_row([
                self.SEASONS[i],
                self.AGE[i],
                self.TEAM[i],
                self.PPG[i][0],
                self.RPG[i][0],
                self.APG[i][0],
                self.FT_PERCENT[i][0],
                self.EFG_PERCENT[i][0],
                self.PER[i][0],
                self.TS[i][0],
                self.M_VALUE[i]])

        out_raw_table = "\nRaw\n" + str(raw_table) + "\n"
        return out_raw_table

    # Normalized stats table
    def build_norm_table(self):
        norm_table = PrettyTable()
        norm_table.field_names = self.get_table_field_names()

        for i in range(len(self.SEASONS)):
            norm_table.add_row([
                self.SEASONS[i],
                self.AGE[i],
                self.TEAM[i],
                self.PPG[i][1],
                self.RPG[i][1],
                self.APG[i][1],
                self.FT_PERCENT[i][1],
                self.EFG_PERCENT[i][1],
                self.PER[i][1],
                self.TS[i][1],
                self.M_VALUE[i]])

        out_norm_table = "\nNormalized\n" + str(norm_table) + "\n"
        return out_norm_table

    # M Value table
    def build_m_value_table(self, window_size):
        idx = self.get_prime(window_size=window_size)

        name = self.name
        seasons = self.SEASONS[idx: idx + window_size]
        ages = self.AGE[idx: idx + window_size]
        teams = self.TEAM[idx: idx + window_size]
        m_values = self.M_VALUE[idx: idx + window_size]

        prime_table = PrettyTable()
        prime_table.field_names = ["Year", "Age", "Team", "M_VALUE"]

        for i in range(len(seasons)):
            prime_table.add_row([seasons[i], ages[i], teams[i], m_values[i]])

        table_title = "\n" + name + " " + str(window_size) + "-year prime\n"
        out_prime_table = table_title + str(prime_table) + "\n"
        return out_prime_table

    # Create output directory for each player
    def get_player_dir(self):
        name = self.name
        player_output_dir = os.path.join(OUTPUT_DIR, name)
        if not os.path.exists(player_output_dir):
            os.makedirs(player_output_dir)

        return player_output_dir

    # Plot raw stats and normalized stats
    def plot_results(self):
        name = self.name
        player_dir = self.get_player_dir()

        stat_types = {
            "Raw": 0,
            "Normalized": 1
        }

        for st in stat_types:
            stat_col = stat_types[st]

            # create a plot figure with subplots
            plt.figure(figsize=(20, 10))
            plt.suptitle(name + "_" + str(st))

            subplot_idx = 1
            for key in self.STAT_CATS:
                stat = self.STAT_CATS[key]

                plt.subplot(3, 3, subplot_idx)
                plt.plot(self.SEASONS, self._get_column(stat, stat_col))
                plt.title(key)
                plt.xticks(rotation=45)
                plt.subplots_adjust(hspace=0.5)
                plt.grid()

                subplot_idx += 1

            # save plot
            plot_filename = name + "_Plots_" + str(st) + ".png"
            plot_file = os.path.join(player_dir, plot_filename)
            plt.savefig(plot_file)
            plt.close()

    # Write table output to file
    def save_tables(self, table):
        name = self.name
        player_dir = self.get_player_dir()

        table_filename = name + "_Table Results.txt"
        out_file = os.path.join(player_dir, table_filename)

        with open(out_file, "a") as f:
            f.write(table)