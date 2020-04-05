"""
Michael Patel
April 2020

File description:
    Collect data and visualize for 21st century NBA MVPs
"""
################################################################################
# Imports
import os
from multiprocessing import Pool
import shutil
import pandas as pd


################################################################################
URL_CSV = os.path.join(os.getcwd(), "data\\url.csv")
OUTPUT_DIR = os.path.join(os.getcwd(), "results")


################################################################################
# deletes a given directory
def delete_dir(d):
    if os.path.exists(d):
        shutil.rmtree(d)


# create and return list of Basketball Reference URLs
def get_player_urls():
    url_list = []

    column_header = "URL"
    data_df = pd.read_csv(URL_CSV, usecols=[column_header])

    for index, row in data_df.iterrows():
        url_list.append(row[column_header])

    return url_list


# collect data
def run(url):


################################################################################
# Main
if __name__ == "__main__":
    # initial cleanup
    delete_dir(OUTPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # get list of Basketball Reference URLs
    URLS = get_player_urls()

    # multiprocessing
    processes = Pool(processes=len(URLS))
    processes.map(run, URLS)
    processes.close()


