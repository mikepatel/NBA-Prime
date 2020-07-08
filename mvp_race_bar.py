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
    
