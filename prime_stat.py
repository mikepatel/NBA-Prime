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

# find "Per Game" table
table = soup.find("table", id="per_game")  # find() = find a specific vs find_all()
table_body = table.find("tbody")
rows = table_body.find_all("tr")


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
STAT = "pts_per_g"
prime, value = get_prime(CAREER_STATS, SLIDE_WINDOW, STAT)
print("\nPrime years: {}".format(prime))
print("{}: {}\n".format(STAT.upper(), value))


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








