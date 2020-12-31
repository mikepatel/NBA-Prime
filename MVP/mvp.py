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
import seaborn as sns


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

    return value


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
    print(mvp_df.sort_values("HITP", ascending=False))

    # create racing bar chart
