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

soup = BeautifulSoup(data, "html.parser")
print(soup.title.text.strip())

# find "Per Game" table
table = soup.find("table", id="per_game")  # find() = find a specific vs find_all()
table_body = table.find("tbody")
rows = table_body.find_all("tr")

CAREER_STATS = {}
SEASONS = []
PPG = []
APG = []
RPG = []

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

        SEASONS.append(season)
        PPG.append(ppg)
        RPG.append(rpg)
        APG.append(apg)

    except AttributeError:
        continue

CAREER_STATS["season"] = SEASONS
CAREER_STATS["ppg"] = PPG
CAREER_STATS["rpg"] = RPG
CAREER_STATS["apg"] = APG


def get_prime(stat, window_size):
    value = 0.0
    idx = 0

    for i in range(len(CAREER_STATS[stat])+1-window_size):
        avg = np.mean(CAREER_STATS[stat][i: i+window_size])

        if avg > value:
            value = avg
            idx = i

    seasons = SEASONS[idx: idx+window_size]

    return seasons, value


SLIDE_WINDOW_SIZE = 4
STAT = "ppg"
years, stat_value = get_prime(STAT, SLIDE_WINDOW_SIZE)
years = ", ".join(years)
print("\n{} year prime: {}".format(SLIDE_WINDOW_SIZE, years))
print("{}: {:.4f}\n".format(STAT.upper(), stat_value))

'''
CAREER_STATS = []

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

        #
        CAREER_STATS.append({"season": season,
                             "pts_per_g": ppg,
                             "trb_per_g": rpg,
                             "ast_per_g": apg})
    except AttributeError:
        continue


def get_prime(stats_list, slide_window, stat):
    candidates = []
    # generate list of candidates
    for i in range(len(stats_list)+1-slide_window):
        batch = stats_list[i: i+slide_window]
        SEASONS = []
        VALUE = []

        for year in batch:
            SEASONS.append(year["season"])
            VALUE.append(year[stat])

        avg_value = np.mean(VALUE)
        candidates.append({"window": SEASONS, stat: avg_value})

    # find prime
    value = 0.0
    prime = []
    for c in candidates:
        if c[stat] > value:
            value = c[stat]
            prime = c["window"]

    return prime, value


SLIDE_WINDOW = 3  # number of prime years parameter
STAT = "ast_per_g"
prime, value = get_prime(CAREER_STATS, SLIDE_WINDOW, STAT)
prime = ", ".join(prime)  # concatenate items in list
print("\n{} prime years: {}".format(SLIDE_WINDOW, prime))
print("{}: {:.4f}\n".format(STAT.upper(), value))
'''


################################################################################
players_file = os.path.join(os.getcwd(), "players list.csv")
print(players_file)

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

print(Players)
for player in Players:
    print(Players[player])  # contents of dictionary item








