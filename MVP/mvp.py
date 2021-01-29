"""
Michael Patel
December 2020

File description:
    Generate a CSV for 21st century NBA MVP campaigns
    Generate a racing bar chart for 21st century NBA MVP campaigns

"""
################################################################################
# Imports
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation


################################################################################
# normalize
def normalize(df):
    df = df.copy()
    for col in df.columns:
        if col == "Points" or col == "Rebounds" or col == "Assists" or col == "Win Pct" or col == "Memorability":
            numerator = df[col] - min(df[col])
            denominator = max(df[col]) - min(df[col])
            df[col] = numerator / denominator

    return df


# calculate HITP
def calculate_hitp(data_row):
    w_pts = 1.0
    w_rebs = 1.0
    w_asts = 1.0
    w_wins = 1.0
    w_mem = 1.0
    w_another = 1.0

    value = np.sum([
        w_pts*data_row["Points"],
        w_rebs*data_row["Rebounds"],
        w_asts*data_row["Assists"],
        w_wins*data_row["Win Pct"],
        w_mem*data_row["Memorability"],
        w_another*data_row["Another"]
    ])

    value = np.around(value, decimals=4)
    return value


# plot bar chart of HITP
def plot_bar(csv_filepath, sort, save_dir, filename):
    df = pd.read_csv(csv_filepath)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(20, 15))

    colours = cm.rainbow(np.linspace(0, 1, len(df)))

    if sort:
        df = df.sort_values("HITP", ascending=False, ignore_index=True)

    xlabels = []
    for index, row in df.iterrows():
        label = row["Name"] + " " + str(row["Year"])
        xlabels.append(label)

    df["HITP"] = np.around(df["HITP"], decimals=4)

    ax.clear()
    ax.bar(xlabels, df["HITP"], color=colours)
    ax.set_title("21st Century NBA MVPs")
    ax.set_xticklabels(xlabels, rotation=30, horizontalalignment="right")
    ax.set_ylabel("HITP")

    for i in range(len(df)):
        ax.annotate(f'{df.loc[i, "HITP"]}', (i-0.3, df.loc[i, "HITP"]+0.01))

    filepath = os.path.join(save_dir, filename)
    plt.savefig(filepath)


# plot racing bar chart of HITP
def plot_racing_bar(csv_filepath, save_dir):
    df = pd.read_csv(csv_filepath)
    size_df = len(df)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(20, 15))
    colours = cm.rainbow(np.linspace(0, 1, size_df))

    def draw_chart(frame):
        df = pd.read_csv(csv_filepath)
        df = df.head(frame)
        df["HITP"] = np.around(df["HITP"], decimals=4)

        df["Rank"] = df["HITP"].rank(method="first")

        # plot
        ax.clear()
        ax.barh(df["Rank"], df["HITP"], color=colours)
        ax.set_title("21st Century NBA MVPs")
        [spine.set_visible(False) for spine in ax.spines.values()]  # remove border around figure
        ax.get_xaxis().set_visible(False)  # hide x-axis
        ax.get_yaxis().set_visible(False)  # hide y-axis

        for index, row in df.iterrows():
            ax.text(x=0, y=row["Rank"], s=str(row["Year"]) + " " + row["Name"], ha="right", va="center")  # base axis
            ax.text(x=row["HITP"], y=row["Rank"], s=str(row["HITP"]), ha="left", va="center")

    gif_filepath = os.path.join(save_dir, "racing_bar_mvp.gif")
    animator = animation.FuncAnimation(fig, draw_chart, frames=len(df), interval=1500)
    animator.save(gif_filepath, writer="imagemagick")


################################################################################
# Main
if __name__ == "__main__":
    # directories
    MVP_DIR = os.path.join(os.getcwd(), "MVP")
    DATA_DIR = os.path.join(MVP_DIR, "data")
    RESULTS_DIR = os.path.join(MVP_DIR, "results")

    # read in csv
    mvp_csv_filename = "mvp_input.csv"
    mvp_csv_filepath = os.path.join(DATA_DIR, mvp_csv_filename)
    mvp_df = pd.read_csv(mvp_csv_filepath, index_col="Year")
    #print(mvp_df)

    # normalize
    norm_df = normalize(mvp_df)

    # calculate HITP index
    hitps = []
    for index, row in norm_df.iterrows():
        hitp = calculate_hitp(row)
        hitps.append(hitp)

    mvp_df["HITP"] = hitps
    #print(mvp_df)

    # write to csv
    output_csv_filename = "mvp_output.csv"
    output_csv_filepath = os.path.join(RESULTS_DIR, output_csv_filename)
    mvp_df.to_csv(output_csv_filepath)

    # print out rankings
    #print(mvp_df.sort_values("HITP", ascending=False))

    # create racing bar chart
    plot_racing_bar(
        csv_filepath=output_csv_filepath,
        save_dir=RESULTS_DIR
    )

    # create bar chart
    plot_bar(
        csv_filepath=output_csv_filepath,
        sort=False,
        save_dir=RESULTS_DIR,
        filename="bar_mvp"
    )

    # create sorted bar chart
    plot_bar(
        csv_filepath=output_csv_filepath,
        sort=True,
        save_dir=RESULTS_DIR,
        filename="sorted_bar_mvp"
    )
