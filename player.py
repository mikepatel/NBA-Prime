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

        page = re.sub('<!--|-->', "", str(page))

        # html soup
        self.soup = BeautifulSoup(page, "html.parser")

        # player name
        self.name = self.get_name()

        # build dict for stats
        self.STATS = {
            "Season": [],  # season, xxxx-xx
            "Age": [],  # age at start of season
            "Team": [],  # team
            "Points": [],  # points per game
            "Rebounds": [],  # rebounds per game
            "Assists": [],  # assists per game
            "FT%": [],  # FT% per game
            "eFG%": [],  # eFG% per game
            "PER": [],  # PER per game
            "TS%": [],  # TS% per game
            "M_VALUE": []  # m value, custom statistic calculated for each season
        }

        # initialize stats dataframes
        self.stats_df = pd.DataFrame()
        self.norm_stats_df = pd.DataFrame()
        self.m_value_df = pd.DataFrame()

    # return player's name
    def get_name(self):
        name = self.soup.title.text.strip()
        name, _ = name.split("Stats")
        name = name.strip()
        return name

    # !! CONCERNED WITH JUST REGULAR SEASON FOR RIGHT NOW !!
    # parse html data for stats
    def get_stats(self):
        # regular season
        self.get_reg_season_stats()
        self.update_stats_df()

        # playoffs
        # self.get_playoff_stats()

    # all regular season stats
    def get_reg_season_stats(self):
        self.get_reg_season_trad_stats()  # traditional stats
        self.get_reg_season_advanced_stats()  # advanced stats

    # all playoff stats
    def get_playoff_stats(self):
        print("To do")
        return self

    # regular season traditional stats
    # Seasons, Ages, Teams, Points, Rebounds, Assists, FT %, eFG %
    def get_reg_season_trad_stats(self):
        rows = self.get_table_rows(table_type="regular season traditional")

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
                self.STATS["Season"].append(season)
                self.STATS["Age"].append(age)
                self.STATS["Team"].append(team)

                # update player's traditional stats
                self.STATS["Points"].append(ppg)
                self.STATS["Rebounds"].append(rpg)
                self.STATS["Assists"].append(apg)
                self.STATS["FT%"].append(ft_pct)
                self.STATS["eFG%"].append(efg_pct)

            except AttributeError as e:
                if "attribute 'a'" in str(e):  # 'Season' is not a hyperlink
                    continue

    # regular season advanced stats
    # PER, TS%
    def get_reg_season_advanced_stats(self):
        rows = self.get_table_rows(table_type="regular season advanced")
        for row in rows:
            try:
                # PER
                per = self.read_stat_from_table(row, "per")
                # print("PER: ", per)

                # TS
                ts = self.read_stat_from_table(row, "ts_pct")
                # print("TS: ", ts)

                # update player's advanced stats
                self.STATS["PER"].append(per)
                self.STATS["TS%"].append(ts)

            except AttributeError:
                continue  # for now

    # scrape and return table data rows
    def get_table_rows(self, table_type):
        if table_type == "regular season traditional":
            table = self.soup.find("table", {"id": "per_game"})  # "Per Game" table => Regular Season
        elif table_type == "regular season advanced":
            table = self.soup.find("table", {"id": "advanced"})  # find "Advanced" table
        else:
            print("\nCannot find table: {}".format(table_type))
            quit()

        table_body = table.find("tbody")
        rows = table_body.find_all("tr")
        return rows

    # reads a particular stat value from html data
    @staticmethod
    def read_stat_from_table(row, feature):
        try:
            x = float(row.find("td", {"data-stat": feature}).text.strip())
            return x
        except AttributeError as e:
            if "attribute 'text'" in str(e):
                return float(0.0)

    # update stats df
    def update_stats_df(self):
        self.stats_df = pd.DataFrame({k: pd.Series(v) for k, v in self.STATS.items()})

    # update normalized stats df
    def update_norm_stats_df(self):
        for key in self.STATS:
            self.norm_stats_df[key] = self.normalize(self.stats_df[key])

    # update m_value stats df
    def update_m_value_stats_df(self):
        print(self.m_value_df)

    # calculate min-max normalization
    @staticmethod
    def normalize(stat_col):
        col_name = stat_col.name
        if col_name == "Season" or col_name == "Age" or col_name == "Team":
            return stat_col
        else:
            col_min = np.min(stat_col)
            col_max = np.max(stat_col)
            denom = col_max - col_min

            # check if denominator is 0
            if denom == 0.0:
                return stat_col
            else:
                # normalize stat value
                numer = stat_col - col_min
                norm_df = numer / denom
                norm_df = np.round(norm_df, decimals=4)

                return norm_df

    # calculate m values
    def calculate_m_value(self):
        # normalize first
        self.update_norm_stats_df()

        # weight values
        w1 = 0.1  # points
        w2 = 0.1  # rebounds
        w3 = 0.1  # assists
        w4 = 0.1  # FT percentage
        w5 = 0.1  # eFG percentage
        w6 = 0.1  # PER
        w7 = 0.1  # TS

        # calculate an m value for each season
        for index, row in self.norm_stats_df.iterrows():
            m_value = np.sum([
                w1*row["Points"],
                w2*row["Rebounds"],
                w3*row["Assists"],
                w4*row["FT%"],
                w5*row["eFG%"],
                w6*row["PER"],
                w7*row["TS%"]
            ])
            m_value = np.round(m_value, decimals=4)
            self.norm_stats_df.loc[index, "M_VALUE"] = m_value
            self.stats_df.loc[index, "M_VALUE"] = m_value

    #
    def get_prime(self, window_size):
        avg_m_value = 0.0
        idx = 0

        var_series = self.norm_stats_df["M_VALUE"].rolling(window_size).var()
        mean_series = self.norm_stats_df["M_VALUE"].rolling(window_size).mean()

        for index, value in var_series.iteritems():
            if value < 0.004:
                if mean_series[index] > avg_m_value:
                    avg_m_value = mean_series[index]
                    idx = index

        """
        for i in range(window_size-1, len(var_series)):
            if var_series[i] < 0.0015:
                if mean_series[i] > avg_m_value:
                    avg_m_value = mean_series[i]
                    idx = i-window_size+1
        """
        self.m_value_df = self.stats_df.loc[idx-window_size+1:idx]




    ########################################





    # returns specified column of values
    @staticmethod
    def _get_column(matrix, c_idx):
        return [row[c_idx] for row in matrix]

    """

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
    """