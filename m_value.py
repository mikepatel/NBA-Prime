"""
Michael Patel
April 2019

version: Python 3.6.5

File Description:

Notes:
    - scraping from Basketball Reference
    - use 'm_value' statistic for each season
        - 'm_value' is constructed from a weighted combination of several statistics such as:
            - points, rebounds, assists
            - PER, true shooting, FT shooting
            - !! winning awards (MVP, title, Finals MVP, etc.) should factor into calculation of m_value
    - !! CONCERNED WITH JUST REGULAR SEASON !!
    - perform feature scaling (0/1 normalization) on stats before computing m_value
    - How best to store all stats data? How to pipe into model?
    - How much does 'consistency' matter for a player's prime? => variance over prime window
        - Having trouble with Steph => need more features?
            - eFG%: "efg_pct"
            - https://www.basketball-reference.com/about/factors.html  Dean Oliver 4 factors
            - RNN, LSTM
    - Can a player's prime include their first year on a team? (discounting injuries, suspensions, etc.)
        - How much does team chemistry factor into a player's prime?
        - What is the relationship (balance) between player and team successes that define a player's prime?
    - make concurrent url requests => multiple threads
        - GUI, matplotlib, Tkinter vs in main loop
        - threading vs multiprocessing
        - USING MULTIPROCESSING INSTEAD OF THREADING

"""

################################################################################
# IMPORTs
import os
import numpy as np
import re
import multiprocessing
import shutil
import csv
from bs4 import BeautifulSoup
import urllib  # standard library
import urllib.request
from prettytable import PrettyTable
import matplotlib.pyplot as plt


################################################################################
OUTPUT_DIR = os.path.join(os.getcwd(), "Results")
PLAYERS_CSV = os.path.join(os.getcwd(), "players list.csv")
#PLAYERS_CSV = os.path.join(os.getcwd(), "steph.csv")


# deletes a given directory
def delete_dir(d):
    if os.path.exists(d):
        shutil.rmtree(d)


# creates list of Basketball Reference URLs
def build_player_list():
    url_list = []

    with open(PLAYERS_CSV, newline="") as f:
        csv_reader = csv.reader(f, delimiter=",")

        line_count = 0

        for row in csv_reader:
            if line_count == 0:  # column names
                line_count += 1
            else:
                url = str(row[1])  # Basketball Reference urls
                url_list.append(url)
                line_count += 1

    return url_list


################################################################################
class Player:
    def __init__(self, url):
        self.url = url
        with urllib.request.urlopen(self.url) as response:
            page = response.read()

        self.soup = BeautifulSoup(re.sub("<!--|-->", "", str(page)), "html.parser")

        # player name
        self.name = self.get_name()

        self.SEASONS = []  # year xxxx-xx
        self.AGE = []  # age at start of season
        self.TEAM = []  # NBA team

        # stats of interest
        self.PPG = []  # points per
        self.RPG = []  # rebounds per
        self.APG = []  # assists per
        self.PER = []  # player efficiency rating per
        self.TS = []  # true shooting percentage per
        self.FT_PERCENT = []  # free throw percentage per
        self.EFG_PERCENT = []  # effective field goal percentage per

        # custom statistic
        # calculated for each season
        self.M_VALUE = []

        # build dict for stat categories
        self.STAT_CATS = {
            "Points": self.PPG,  # points
            "Rebounds": self.RPG,  # rebounds
            "Assists": self.APG,  # assists
            "FT Percentage": self.FT_PERCENT,  # FT%
            "eFG Percentage": self.EFG_PERCENT,  # eFG%
            "PER": self.PER,  # PER
            "TS": self.TS  # TS%
        }

    # returns player's name
    def get_name(self):
        name = self.soup.title.text.strip()
        name, _ = name.split("Stats")
        name = name.strip()
        return name

    # returns specified column of values
    @staticmethod
    def get_column(matrix, c_idx):
        return [row[c_idx] for row in matrix]

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

    # reads a particular stat value from html data
    @staticmethod
    def read_stat_from_table(row, feature):
        try:
            x = float(row.find("td", {"data-stat": feature}).text.strip())
            return x
        except AttributeError as e:
            if "attribute 'text'" in str(e):
                return float(0.0)

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

    # Seasons, Ages, Teams
    # Points, Rebounds, Assists, FT%, eFG%
    def get_reg_season_trad_stats(self):
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
                self.STAT_CATS["Points"].append([ppg])
                self.STAT_CATS["Rebounds"].append([rpg])
                self.STAT_CATS["Assists"].append([apg])
                self.STAT_CATS["FT Percentage"].append([ft_pct])
                self.STAT_CATS["eFG Percentage"].append([efg_pct])

            except AttributeError as e:
                if "attribute 'a'" in str(e):  # 'Season' is not a hyperlink
                    continue

    # PER, TS%
    def get_reg_season_advanced_stats(self):
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
                self.STAT_CATS["PER"].append([per])
                self.STAT_CATS["TS"].append([ts])

            except AttributeError:
                continue  # for now

    def get_reg_season_stats(self):
        self.get_reg_season_trad_stats()  # Regular Season: seasons, age, team
                                            # points, rebounds, assists, FT%, eFG%
        self.get_reg_season_advanced_stats()  # Regular Season: PER, TS%

    # !! CONCERNED WITH JUST REGULAR SEASON !!
    # builds stat value lists from html data
    def get_stats(self):
        self.get_reg_season_stats()

    # Calculates 'm_value' per player season
    def calculate_m_value(self):
        # normalize stats
        for key in self.STAT_CATS:
            self.STAT_CATS[key] = self.normalize(self.STAT_CATS[key])

        """
        self.PPG = self.normalize(self.PPG)
        self.RPG = self.normalize(self.RPG)
        self.APG = self.normalize(self.APG)
        self.FT_PERCENT = self.normalize(self.FT_PERCENT)
        self.EFG_PERCENT = self.normalize(self.EFG_PERCENT)
        self.PER = self.normalize(self.PER)
        self.TS = self.normalize(self.TS)
        """

        # weight values
        w1 = 0.1  # points
        w2 = 0.1  # rebounds
        w3 = 0.1  # assists
        w4 = 0.1  # FT percentage
        w5 = 0.1  # PER
        w6 = 0.1  # TS
        w7 = 0.1  # eFG percentage

        for i in range(len(self.SEASONS)):
            m_value = np.sum([
                w1*self.PPG[i][1],
                w2*self.RPG[i][1],
                w3*self.APG[i][1],
                w4*self.FT_PERCENT[i][1],
                w5*self.PER[i][1],
                w6*self.TS[i][1],
                w7*self.EFG_PERCENT[i][1]
            ])
            m_value = np.round(m_value, decimals=4)
            self.M_VALUE.append(m_value)

    # Field names for PrettyTable output
    @staticmethod
    def get_table_field_names():
        return [
            "Year", "Age", "Team", "Points", "Rebounds",
            "Assists", "FT %", "PER", "TS", "eFG %", "M_VALUE"
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
                self.PER[i][0],
                self.TS[i][0],
                self.EFG_PERCENT[i][0],
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
                self.PER[i][1],
                self.TS[i][1],
                self.EFG_PERCENT[i][1],
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

        stat_cats = [
            ["Points", self.PPG],
            ["Rebounds", self.RPG],
            ["Assists", self.APG],
            ["FT %", self.FT_PERCENT],
            ["PER", self.PER],
            ["TS", self.TS],
            ["eFG %", self.EFG_PERCENT]
        ]

        for st in stat_types:
            stat_col = stat_types[st]
            # create a plot figure with subplots
            plt.figure(figsize=(20, 10))
            plt.suptitle(name + "_" + str(st))

            for idx in range(7):
                subplot_idx = idx + 1

                stat = stat_cats[idx][1]

                plt.subplot(3, 3, subplot_idx)
                plt.plot(self.SEASONS, self.get_column(stat, stat_col))
                plt.title(stat_cats[idx][0])
                plt.xticks(rotation=45)
                plt.subplots_adjust(hspace=0.5)
                plt.grid()

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


################################################################################
# calculates players' primes and returns results in table format and plots
def run(url):
    # break_line = "\n####################################################################################"
    p = Player(url)

    # Player name
    name = p.get_name()
    out_name = "\n" + name + "\n"

    p.get_stats()
    p.calculate_m_value()
    raw_table = p.build_raw_table()  # Raw stats
    norm_table = p.build_norm_table()  # Normalized stats

    # ?-year Prime stats
    WINDOW_SIZE = 3
    prime_table = p.build_m_value_table(WINDOW_SIZE)  # m_values

    # print out table results at end
    output = [
        # break_line,
        out_name,
        raw_table,
        norm_table,
        prime_table
    ]
    output = "".join(output)

    # Write table output to file
    p.save_tables(output)

    # Plot Raw and Normalized stats
    p.plot_results()


################################################################################
# Main
if __name__ == "__main__":
    delete_dir(OUTPUT_DIR)

    URLS = build_player_list()

    # multiprocessing
    processes = [multiprocessing.Process(target=run, args=(url,)) for url in URLS]
    for process in processes:
        process.start()
