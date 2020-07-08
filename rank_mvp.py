"""
Michael Patel
May 2020

Project description:
    Use basketball reference data to rank every MVP winner's campaign since 2000

File description:
    Use basketball reference data to rank every MVP winner's campaign since 2000
"""
################################################################################
# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from constants import *

################################################################################
# Main
if __name__ == "__main__":
    # Read in CSV
    df = pd.read_csv(MVP_CSV)

    norm_df = df.copy()

    # Normalize data using Min-Max
    column_names = list(norm_df.columns)
    for col in column_names:
        if col == "Year" or \
                col == "Name" or \
                col == "HITP Index" or \
                col == "URL":  # doesn't make sense to normalize these columns
            pass
        else:
            min = np.min(norm_df[col])
            max = np.max(norm_df[col])

            denominator = max - min

            if denominator == 0.0:
                pass
            else:
                numerator = norm_df[col] - min
                norm = numerator / denominator
                norm = np.round(norm, decimals=4)

                norm_df[col] = norm

    # Calculate HITP index
    # weights
    w_pts = 0.7
    w_rebs = 0.5
    w_asts = 0.5
    w_wins = 1
    w_memorability = 1
    w_another = 1

    for index, row in norm_df.iterrows():
        hitp_index = np.sum([
            w_pts*row["Points"],
            w_rebs*row["Rebounds"],
            w_asts*row["Assists"],
            w_wins*row["Wins"],
            w_memorability*row["Memorability"],
            w_another*row["Another"]
        ])

        hitp_index = np.round(hitp_index, decimals=4)

        df.loc[index, "HITP Index"] = hitp_index

    # Write to CSV
    #df = df.sort_values(by="HITP Index", ascending=False)
    df.to_csv(MVP_UNRANKED_CSV, index=False)

    # Plot results
    chart_df = df.sort_values("HITP Index", ascending=False)
    x_labels = []
    for index, row in chart_df.iterrows():
        label = str(row["Name"]) + " " + str(row["Year"])
        x_labels.append(label)

    # colour bars differently
    colours = cm.rainbow(np.linspace(0, 1, len(x_labels)))

    # build plot
    plt.style.use("dark_background")
    plt.figure(figsize=(20, 10))
    plt.bar(x_labels, chart_df["HITP Index"], color=colours, zorder=2)
    plt.title("21st Century MVPs")
    plt.xlabel("MVP")
    plt.xticks(rotation=30, horizontalalignment="right")
    plt.ylabel("HITP Index")
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.grid(axis="y", linewidth=0.3)

    # save plot
    plot_filename = "mvp_plot.png"
    plot_file = os.path.join(os.getcwd(), "mvp_results\\" + plot_filename)
    plt.savefig(plot_file)
    plt.close()
