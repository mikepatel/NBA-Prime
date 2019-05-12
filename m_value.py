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
# Imports
import os
import multiprocessing
import shutil
import pandas as pd

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
    p.get_prime(3)

    #print(p.name)
    #print(p.stats_df)
    #print(p.norm_stats_df)
    #print(p.m_value_df)

    p.save_results()
    #quit()

    """
    raw_table = p.build_raw_table()  # Raw stats
    norm_table = p.build_norm_table()  # Normalized stats

    # ?-year Prime stats
    window_size = 3
    prime_table = p.build_m_value_table(window_size)  # m_values

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
    """


################################################################################
# Main
if __name__ == "__main__":
    # initial cleanup
    delete_dir(OUTPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # get list of Basketball Reference URLs
    URLS = get_player_urls()

    # multiprocessing
    processes = [multiprocessing.Process(target=run, args=(url,)) for url in URLS]
    for process in processes:
        process.start()
