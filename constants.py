"""
Michael Patel
May 2019

version: Python 3.6.5

File Description:

Notes:

"""


################################################################################
# Imports
import os


################################################################################
PLAYERS_CSV = os.path.join(os.getcwd(), "data\\players list.csv")  # input
OUTPUT_DIR = os.path.join(os.getcwd(), "Results")  # output

MVP_CSV = os.path.join(os.getcwd(), "data\\mvp.csv")
MVP_RESULTS_CSV = os.path.join(os.getcwd(), "mvp_results\\mvp_results.csv")
MVP_UNRANKED_CSV = os.path.join(os.getcwd(), "mvp_results\\mvp_unranked.csv")
