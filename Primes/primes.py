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
from multiprocessing import Pool


################################################################################
# directories
PRIMES_DIR = os.path.join(os.getcwd(), "Primes")
DATA_DIR = os.path.join(PRIMES_DIR, "data")
RESULTS = os.path.join(PRIMES_DIR, "results")


################################################################################
# get CLI arguments
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", help="Analyze stats for current players (2010-2020)", action="store_true")
    parser.add_argument("--legacy", help="Analyze stats for retired players", action="store_true")
    arguments = parser.parse_args()

    # check if there are any CLI arguments
    if not arguments.current and not arguments.legacy:
        print(f'\nPlease provide an argument:')
        parser.print_help()
        sys.exit(1)

    else:
        return arguments


# get data csv filename based on CLI arguments
def get_data_filename(arguments):
    if arguments.current:
        filename = "current_players.csv"
        return filename

    elif arguments.legacy:
        filename = "legacy_players.csv"
        return filename

    else:
        print(f'\nPlease provide an argument:')
        sys.exit(1)


################################################################################
# Main
if __name__ == "__main__":
    # get CLI arguments
    args = get_arguments()

    # select which csv to use
    data_filename = get_data_filename(args)  # get data csv filename
    #print(data_filename)

    # MULTIPROCESSING WORK: FOR EACH PLAYER
    # For each player, scrape Basketball Reference and create a csv with raw stats
    # multiprocessing work

    # For each player, for each season, calculate M_VALUE
    # multiprocessing work

    # For each player, calculate n-year prime using M_VALUES
    # multiprocessing work

    # For each player, create a 3x3 plot of their stats
    # multiprocessing work
    # Points, Rebounds, Assists
    # Games
    # FT%, PER, TS%, eFG%
    # M_VALUE

    # FOR CURRENT PLAYERS (2010-2020)
    if args.current:
        # Aggregate M_VALUES for all players for all seasons

        # Create a heatmap for all players for all seasons based on M_VALUES
        print("heatmap")

    quit()
