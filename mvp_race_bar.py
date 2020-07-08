"""
Michael Patel
July 2020

Project description:
    Use basketball reference data to rank every MVP winner's campaign since 2000

File description:
    Use basketball reference data to rank every MVP winner's campaign since 2000
    and visualize in a "racing" bar chart
"""
################################################################################
# Imports
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import matplotlib.animation as animation

from constants import *


################################################################################
# Main
if __name__ == "__main__":
    # read in CSV data
    df = pd.read_csv(MVP_UNRANKED_CSV)

    # create plot figure
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(15, 10))

    # function to be called repeatedly to draw on canvas
    def draw_chart(frame):
        # read in CSV data
        df = pd.read_csv(MVP_UNRANKED_CSV)

        # rank highest HITP index to lowest
        df = df.head(frame)
        df["Rank"] = df["HITP Index"].rank(method="first", ascending=True)
        df = df.sort_values(by="Rank", ascending=False)
        df = df.reset_index(drop=True)

        # plot
        ax.clear()
        colours = cm.rainbow(np.linspace(0, 1, len(df)))
        ax.barh(df["Rank"], df["HITP Index"], color=colours)
        ax.set_title("21st Century MVPs by HITP Index")
        [spine.set_visible(False) for spine in ax.spines.values()]  # remove border around figure
        ax.get_xaxis().set_visible(False)  # hide x-axis
        ax.get_yaxis().set_visible(False)  # hide y-axis

        for index, row in df.iterrows():
            ax.text(x=0, y=row["Rank"], s=str(row["Year"]) + " " + row["Name"], ha="right", va="center")
            ax.text(x=row["HITP Index"], y=row["Rank"], s=row["HITP Index"], ha="left", va="center")

    # animation
    gif_filepath = os.path.join(os.getcwd(), "mvp_results\\rank.gif")
    animator = animation.FuncAnimation(fig, draw_chart, frames=range(len(df)), interval=800)
    animator.save(gif_filepath, writer="imagemagick")
