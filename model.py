"""
Michael Patel
April 2019

Python 3.6.5

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
# Imports
import os
from multiprocessing import Pool
import shutil
import pandas as pd
import time

from player import Player  # custom class
from constants import *


################################################################################
# deletes a given directory
def delete_dir(d):
    if os.path.exists(d):
        shutil.rmtree(d)


# create and return list of Basketball Reference URLs
def get_player_urls():
    url_list = []

    column_header = "Basketball Reference URL"
    data_df = pd.read_csv(PLAYERS_CSV, usecols=[column_header])

    for index, row in data_df.iterrows():
        url_list.append(row[column_header])

    return url_list


################################################################################
# calculates players' primes and returns results in table format and plots
def run(url):
    p = Player(url)

    p.get_stats()
    p.calculate_m_value()
    p.get_prime(window_size=3)

    p.save_results()
    p.plot_results()


################################################################################
# Main
if __name__ == "__main__":
    # start time
    start = time.time()
    print("Running...")

    # initial cleanup
    delete_dir(OUTPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # get list of Basketball Reference URLs
    URLS = get_player_urls()

    # multiprocessing
    processes = Pool(processes=len(URLS))
    processes.map(run, URLS)
    processes.close()

    # runtime
    runtime = time.time() - start
    print("...Finished!")
    print("Runtime: {:.4f} seconds".format(runtime))
