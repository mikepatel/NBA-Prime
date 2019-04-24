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
    - How much does 'consistency' matter for a player's prime?
    - Can a player's prime include their first year on a team? (discounting injuries, suspensions, etc.)
        - How much does team chemistry factor into a player's prime?
        - What is the relationship (balance) between player and team successes that define a player's prime?
    - make concurrent url requests => multiple threads

"""

################################################################################
# IMPORTs
from bs4 import BeautifulSoup
import urllib  # standard library
import urllib.request
import numpy as np
from prettytable import PrettyTable
import re
import matplotlib.pyplot as plt
import threading
import time


################################################################################
class Player:
    def __init__(self, url):
        self.url = url
        with urllib.request.urlopen(self.url) as response:
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
            temp_variance = np.var(self.M_VALUE[i: i+window_size])
            #print(i, temp_variance)

            if temp_variance < 0.0015:
                avg_candidate = np.mean(self.M_VALUE[i: i+window_size])

                if avg_candidate > avg_value:
                    avg_value = avg_candidate
                    idx = i

        return idx  # return just the index

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

        # weight values
        w1 = 0.1  # points
        w2 = 0.1  # rebounds
        w3 = 0.1  # assists
        w4 = 0.1  # FT percentage
        w5 = 0.1  # PER
        w6 = 0.1  # TS

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


# called by each thread, calculates players' primes
def run(url):
    break_line = "\n####################################################################################"
    p = Player(url)

    # Player name
    name = p.get_name()
    out_name = "\n" + name + "\n"

    # Player stats
    p.get_stats()

    # Traditional stats
    trad_table = PrettyTable()
    trad_table.field_names = [
        "Year", "Age", "Team", "Points", "Rebounds",
        "Assists", "FT %", "PER", "TS", "M_VALUE"
    ]
    for i in range(len(p.SEASONS)):
        trad_table.add_row([
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

    out_trad_table = "\nTraditional\n" + str(trad_table) + "\n"

    # Normalized stats
    norm_table = PrettyTable()
    norm_table.field_names = [
        "Year", "Age", "Team", "Points", "Rebounds",
        "Assists", "FT %", "PER", "TS", "M_VALUE"
    ]
    for i in range(len(p.SEASONS)):
        norm_table.add_row([
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

    out_norm_table = "\nNormalized\n" + str(norm_table) + "\n"

    # ?-year Prime stats
    WINDOW_SIZE = 3
    idx = p.get_prime(window_size=WINDOW_SIZE)

    seasons = p.SEASONS[idx: idx + WINDOW_SIZE]
    ages = p.AGE[idx: idx + WINDOW_SIZE]
    teams = p.TEAM[idx: idx + WINDOW_SIZE]
    m_values = p.M_VALUE[idx: idx + WINDOW_SIZE]

    prime_table = PrettyTable()
    prime_table.field_names = ["Year", "Age", "Team", "M_VALUE"]
    for i in range(len(seasons)):
        prime_table.add_row([seasons[i], ages[i], teams[i], m_values[i]])

    table_title = "\n" + name + " " + str(WINDOW_SIZE) + "-year prime\n"
    out_prime_table = table_title + str(prime_table) + "\n"

    # print out table results at end
    output = [
        break_line,
        out_name,
        out_trad_table,
        out_norm_table,
        out_prime_table
    ]
    output = "".join(output)
    print(output)

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


# Main
if __name__ == "__main__":
    start = time.time()

    URLS = [
        "https://www.basketball-reference.com/players/j/jamesle01.html",  # LeBron James
        "https://www.basketball-reference.com/players/b/bryanko01.html",  # Kobe Bryant
        "https://www.basketball-reference.com/players/d/duranke01.html",  # Kevin Durant
        "https://www.basketball-reference.com/players/h/hardeja01.html",  # James Harden
        "https://www.basketball-reference.com/players/c/curryst01.html",  # Steph Curry
        "https://www.basketball-reference.com/players/w/wadedw01.html",  # Dwayne Wade
        "https://www.basketball-reference.com/players/n/nowitdi01.html"  # Dirk Nowitzki
    ]

    # use threading for multiple urllib.requests
    # create thread instance for each url in URLS
    threads = [threading.Thread(target=run, args=(url,)) for url in URLS]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    finish = time.time()
    duration = finish - start
    print("\nRuntime: {:.4f}".format(duration))
