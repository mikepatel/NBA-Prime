
import os
import csv

players_file = os.path.join(os.getcwd(), "players list.csv")

URLS = []

with open(players_file, newline="") as f:
    csv_reader = csv.reader(f, delimiter=",")

    line_count = 0

    for row in csv_reader:
        if line_count == 0:  # column names
            line_count += 1
        else:
            url = str(row[1])  # Basketball Reference urls
            URLS.append(url)
            line_count += 1

for url in URLS:
    print(url)
