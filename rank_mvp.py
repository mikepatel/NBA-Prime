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

    for index, row in norm_df.iterrows():
        hitp_index = np.sum([
            w_pts*row["Points"],
            w_rebs*row["Rebounds"],
            w_asts*row["Assists"],
            w_wins*row["Wins"],
            w_memorability*row["Memorability"]
        ])

        df.loc[index, "HITP Index"] = hitp_index

    # Write to CSV
    df = df.sort_values(by="HITP Index", ascending=False)
    df.to_csv(MVP_RESULTS_CSV, index=False)
