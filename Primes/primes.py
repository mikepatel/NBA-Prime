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
from packages import *   # for Python packages and global directories


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


# get data csv filepath based on CLI arguments
def get_data_filepath(arguments):
    if arguments.current:
        # ***** TEMP ***** #
        filename = "test.csv"
        #filename = "current_players.csv"
        filepath = os.path.join(DATA_DIR, filename)
        return filepath

    elif arguments.legacy:
        filename = "legacy_players.csv"
        filepath = os.path.join(DATA_DIR, filename)
        return filepath

    else:
        print(f'\nPlease provide an argument:')
        sys.exit(1)


# get list of player URLs
def get_player_urls(csv_filepath):
    df = pd.read_csv(csv_filepath)
    urls = list(df["Basketball Reference URL"])
    return urls


################################################################################
# run multiprocessing work: For each player, collect stats, calculate values, generate charts
def run(url):
    p = Player(url)
    print(p.url)

    # For each player, scrape Basketball Reference and create a csv with raw stats

    # For each player, for each season, calculate M_VALUE

    # For each player, calculate n-year prime using M_VALUES

    # For each player, create a 3x3 plot of their stats
    # Points, Rebounds, Assists
    # Games
    # FT%, PER, TS%, eFG%
    # M_VALUE


################################################################################
# Main
if __name__ == "__main__":
    # get CLI arguments
    args = get_arguments()

    # select which csv to use
    data_filepath = get_data_filepath(args)  # get data csv filepath

    # MULTIPROCESSING WORK: FOR EACH PLAYER
    player_urls = get_player_urls(data_filepath)

    processes = Pool(processes=len(player_urls))
    processes.map(run, player_urls)
    processes.close()

    # FOR CURRENT PLAYERS (2010-2020)
    if args.current:
        # Aggregate M_VALUES for all players for all seasons

        # Create a heatmap for all players for all seasons based on M_VALUES
        print("heatmap")

    quit()
