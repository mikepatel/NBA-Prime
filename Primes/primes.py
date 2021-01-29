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
from player import Player


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
        #filename = "test.csv"
        filename = "current_players.csv"
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

    # For each player, scrape Basketball Reference and create a csv with raw stats
    p.get_stats()

    # For each player, for each season, calculate M_VALUE
    p.calculate_m_value()

    # For each player, calculate n-year prime using M_VALUES
    p.find_prime(window_size=3)
    #print(p.raw_df)

    # For each player, create a 3x3 plot of their stats
    p.plot_stats()

    # save dataframe to CSV
    p.save_df()


################################################################################
# create a heatmap
def generate_heatmap():
    # aggregate M_VALUES for all players for all seasons
    seasons = [
        "2010-11",
        "2011-12",
        "2012-13",
        "2013-14",
        "2014-15",
        "2015-16",
        "2016-17",
        "2017-18",
        "2018-19",
        "2019-20",
        "2020-21"
    ]

    dirs = os.listdir(RESULTS_DIR)  # names

    xs = []
    for i in range(len(dirs)):  # iterate through players
        d = dirs[i]
        filepath = os.path.join(RESULTS_DIR, d)
        filepath = os.path.join(filepath, d + "_stats.csv")
        df = pd.read_csv(filepath)

        for index, row in df.iterrows():  # iterate through player's df
            if row["Season"] in seasons:
                x = {
                    "Player": d,
                    "Season": row["Season"],
                    "M_VALUE": row["M_VALUE"]
                }

                xs.append(x)

    # create a new df
    heat_df = pd.DataFrame(xs, columns=["Player", "Season", "M_VALUE"])

    # restructure the df
    heat_df = pd.pivot_table(heat_df, values="M_VALUE", index=["Player"], columns=["Season"])
    # print(heat_df)

    # plot heatmap
    plt.style.use("dark_background")
    plt.figure(figsize=(20, 15))
    plt.title("NBA Primes 2010-Present")
    cmap = "YlOrRd"
    sns.heatmap(heat_df, annot=True, cmap=cmap)

    # save heatmap
    heatmap_filename = "heatmap"
    heatmap_filepath = os.path.join(PRIMES_DIR, heatmap_filename)
    plt.savefig(heatmap_filepath)


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
        generate_heatmap()


