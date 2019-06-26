"""
Michael Patel
March 2019

version: Python 3.6.5

File Description:

Notes:
    - BeautifulSoup4
    - use NBA stats website instead of Basketball Reference
    - use 'requests' instead of 'urllib.request'

"""

################################################################################
# IMPORTs
from bs4 import BeautifulSoup
import urllib  # standard library
from selenium import webdriver
import csv
import os
import numpy as np
from prettytable import PrettyTable

################################################################################
# website to crawl
url = "https://stats.nba.com/player/2544/"  # LeBron James

with urllib.request.urlopen(url) as response:
    data = response.read()

soup = BeautifulSoup(data, "html.parser")

temp = soup.title.text.strip()
player_name = temp.split("| ")[1].strip()
print(player_name)

# https://stackoverflow.com/questions/40146128/beautifulsoup-returns-none-even-though-the-element-exists
# https://stackoverflow.com/questions/49766150/when-scraping-data-from-basketball-reference-how-come-certain-tables-are-comment


x = soup.find_all("div", {"class": "nba-stat-table__overflow"})
print(x)

