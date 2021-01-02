"""
Michael Patel
January 2021

Project description:
    To detect (and predict) an NBA player's prime seasons

File description:
    To scrape basketball statistics for each player
    To analyze statistics for each player
    To generate visualizations for each player

"""
################################################################################
# Imports
import os
import sys
import argparse
import numpy as np
import pandas as pd
import seaborn as sns


################################################################################
# directories
PRIMES_DIR = os.path.join(os.getcwd(), "Primes")
DATA_DIR = os.path.join(PRIMES_DIR, "data")
RESULTS = os.path.join(PRIMES_DIR, "results")


################################################################################
# get data csv filename based on CLI arguments
def get_data_filename():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", help="Analyze stats for current players (2010-2020)", action="store_true")
    parser.add_argument("--legacy", help="Analyze stats for retired players", action="store_true")
    args = parser.parse_args()

    if args.current:
        filename = "current_players.csv"
        return filename

    elif args.legacy:
        filename = "legacy_players.csv"
        return filename

    else:
        print(f'\nPlease provide an argument:')
        parser.print_help()
        sys.exit(1)


################################################################################
# Main
if __name__ == "__main__":
    data_filename = get_data_filename()  # get data csv filename

    quit()
