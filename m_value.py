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

"""

################################################################################
# IMPORTs
from bs4 import BeautifulSoup
import urllib  # standard library
import numpy as np
from prettytable import PrettyTable
import re
import matplotlib.pyplot as plt


################################################################################
url = "https://www.basketball-reference.com/players/j/jamesle01.html"  # LeBron James
#url = "https://www.basketball-reference.com/players/b/bryanko01.html"  # Kobe Bryant
#url = "https://www.basketball-reference.com/players/d/duranke01.html"  # Kevin Durant
#url = "https://www.basketball-reference.com/players/h/hardeja01.html"  # James Harden
#url = "https://www.basketball-reference.com/players/c/curryst01.html"  # Steph Curry
#url = "https://www.basketball-reference.com/players/w/wadedw01.html"  # Dwayne Wade
#url = "https://www.basketball-reference.com/players/n/nowitdi01.html"  # Dirk Nowitzki


print("\n------------------------------------------------------------------------")


class Player:
    def __init__(self):
        with urllib.request.urlopen(url) as response:
            page = response.read()

        self.soup = BeautifulSoup(re.sub("<!--|-->", "", str(page)), "html.parser")

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

        # custom statistic
        # calculated for each season
        self.M_VALUE = []

    # return player's name
    def get_name(self):
        name = self.soup.title.text.strip()
        name, _ = name.split("Stats")
        name = name.strip()
        return name

    #
    def get_prime(self, window_size):
        avg_value = 0.0
        idx = 0

        for i in range(len(self.M_VALUE)+1-window_size):
            avg_candidate = np.mean(self.M_VALUE[i: i+window_size])

            if avg_candidate > avg_value:
                avg_value = avg_candidate
                idx = i

        s = self.SEASONS[idx: idx+window_size]
        a = self.AGE[idx: idx+window_size]
        t = self.TEAM[idx: idx+window_size]
        m = self.M_VALUE[idx: idx+window_size]

        return s, a, t, m

    #
    @staticmethod
    def read_stat_from_table(row, feature):
        x = float(row.find("td", {"data-stat": feature}).text.strip())
        return x

    # !! CONCERNED WITH JUST REGULAR SEASON !!
    def get_stats(self):
        # find "Per Game" table => Regular Season
        # 'Traditional' stats
        table = self.soup.find("table", {"id": "per_game"})
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")

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
                #print("Points: ", ppg)

                # rebounds
                rpg = self.read_stat_from_table(row, "trb_per_g")
                #print("Rebounds: ", rpg)

                # assists
                apg = self.read_stat_from_table(row, "ast_per_g")
                #print("Assists: ", apg)

                # FT%
                ft_pct = self.read_stat_from_table(row, "ft_pct")
                #print("FT%: ", ft_pct)

                #
                self.SEASONS.append(season)
                self.AGE.append(age)
                self.TEAM.append(team)
                self.PPG.append([ppg])
                self.RPG.append([rpg])
                self.APG.append([apg])
                self.FT_PERCENT.append([ft_pct])

            except AttributeError:
                continue  # for now

        # find "Advanced" table
        # 'Advanced' stats
        table = self.soup.find("table", {"id": "advanced"})
        table_body = table.find("tbody")
        rows = table_body.find_all("tr")

        for row in rows:
            try:
                # PER
                per = self.read_stat_from_table(row, "per")
                #print("PER: ", per)

                # TS
                ts = self.read_stat_from_table(row, "ts_pct")
                #print("TS: ", ts)

                #
                self.PER.append([per])
                self.TS.append([ts])

            except AttributeError:
                continue  # for now

        # calculate m_value per each season
        # weight values
        w1 = 0.1  # points
        w2 = 0.1  # rebounds
        w3 = 0.1  # assists
        w4 = 0.1  # FT percentage
        w5 = 0.1  # PER
        w6 = 0.1  # TS

        # normalize
        def normalize(stat):
            stat_min = np.min(stat)
            stat_max = np.max(stat)
            den = stat_max - stat_min

            for i in range(len(stat)):
                num = stat[i][0] - stat_min
                x = num / den
                x = np.round(x, decimals=4)
                stat[i].append(x)

            return stat

        self.PPG = normalize(self.PPG)
        self.RPG = normalize(self.RPG)
        self.APG = normalize(self.APG)
        self.FT_PERCENT = normalize(self.FT_PERCENT)
        self.PER = normalize(self.PER)
        self.TS = normalize(self.TS)

        for i in range(len(self.SEASONS)):
            m_value = np.sum([
                w1*self.PPG[i][1],
                w2*self.RPG[i][1],
                w3*self.APG[i][1],
                w4*self.FT_PERCENT[i][1],
                w5*self.PER[i][1],
                w6*self.TS[i][1]
            ])
            m_value = np.round(m_value, decimals=4)
            self.M_VALUE.append(m_value)


# Main
if __name__ == "__main__":
    p = Player()
    name = p.get_name()
    print(name)
    p.get_stats()

    everything_table = PrettyTable()
    everything_table.field_names = [
        "Year", "Age", "Team", "Points", "Rebounds",
        "Assists", "FT %", "PER", "TS", "M_VALUE"
    ]
    for i in range(len(p.SEASONS)):
        everything_table.add_row([
            p.SEASONS[i],
            p.AGE[i],
            p.TEAM[i],
            p.PPG[i][0],
            p.RPG[i][0],
            p.APG[i][0],
            p.FT_PERCENT[i][0],
            p.PER[i][0],
            p.TS[i][0],
            p.M_VALUE[i]])
    print(everything_table)

    normalized_table = PrettyTable()
    normalized_table.field_names = [
        "Year", "Age", "Team", "Points", "Rebounds",
        "Assists", "FT %", "PER", "TS", "M_VALUE"
    ]
    for i in range(len(p.SEASONS)):
        normalized_table.add_row([
            p.SEASONS[i],
            p.AGE[i],
            p.TEAM[i],
            p.PPG[i][1],
            p.RPG[i][1],
            p.APG[i][1],
            p.FT_PERCENT[i][1],
            p.PER[i][1],
            p.TS[i][1],
            p.M_VALUE[i]])
    print(normalized_table)

    """
    out_table = PrettyTable()
    out_table.field_names = ["Year", "Age", "Team", "M_VALUE"]
    for i in range(len(p.SEASONS)):
        out_table.add_row([p.SEASONS[i], p.AGE[i], p.TEAM[i], p.M_VALUE[i]])
    print(out_table)
    """

    # Window
    WINDOW_SIZE = 3
    seasons, ages, teams, m_values = p.get_prime(window_size=WINDOW_SIZE)

    prime_table = PrettyTable()
    prime_table.field_names = ["Year", "Age", "Team", "M_VALUE"]
    for i in range(len(seasons)):
        prime_table.add_row([seasons[i], ages[i], teams[i], m_values[i]])
    print("\n" + name + " " + str(WINDOW_SIZE) + "-year prime")
    print(prime_table)

    """
    # PLOTS
    plt.suptitle(name)

    # Points
    plt.subplot(2, 3, 1)
    plt.plot(p.SEASONS, p.PPG)
    plt.title("Points")
    plt.xticks(rotation=45)
    plt.subplots_adjust(hspace=0.5)
    plt.grid()

    # Rebounds
    plt.subplot(2, 3, 2)
    plt.plot(p.SEASONS, p.RPG)
    plt.title("Rebounds")
    plt.xticks(rotation=45)
    plt.subplots_adjust(hspace=0.5)
    plt.grid()

    # Assists
    plt.subplot(2, 3, 3)
    plt.plot(p.SEASONS, p.APG)
    plt.title("Assists")
    plt.xticks(rotation=45)
    plt.subplots_adjust(hspace=0.5)
    plt.grid()

    # FT %
    plt.subplot(2, 3, 4)
    plt.plot(p.SEASONS, p.FT_PERCENT)
    plt.title("FT %")
    plt.xticks(rotation=45)
    plt.subplots_adjust(hspace=0.5)
    plt.grid()

    # PER
    plt.subplot(2, 3, 5)
    plt.plot(p.SEASONS, p.PER)
    plt.title("PER")
    plt.xticks(rotation=45)
    plt.subplots_adjust(hspace=0.5)
    plt.grid()

    # TS%
    plt.subplot(2, 3, 6)
    plt.plot(p.SEASONS, p.TS)
    plt.title("TS %")
    plt.xticks(rotation=45)
    plt.subplots_adjust(hspace=0.5)
    plt.grid()

    plt.show()
    """
