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

    # Normalize data using Min-Max
    column_names = list(df.columns)
    for col in column_names:
        if col == "Year" or \
                col == "Name" or \
                col == "HITP Index" or \
                col == "URL":  # doesn't make sense to normalize these columns
            pass
        else:
            min = np.min(df[col])
            max = np.max(df[col])

            denominator = max - min

            if denominator == 0.0:
                pass
            else:
                numerator = df[col] - min
                norm = numerator / denominator
                norm = np.round(norm, decimals=4)

                df[col] = norm

    # Calculate HITP index
    # weights
    w_pts = 1
    w_rebs = 1
    w_asts = 1
    w_wins = 1
    w_memorability = 0

    # Write to CSV
    df.to_csv(MVP_RESULTS_CSV)
