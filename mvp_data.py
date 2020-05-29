"""
Michael Patel
May 2020

Project description:
    Use basketball reference data to rank every MVP winner's campaign since 2000

File description:
    To get basketball reference data
"""
################################################################################
# Imports
import os
import pandas as pd

from constants import *


################################################################################
# Main
if __name__ == "__main__":
    df = pd.read_csv(MVP_CSV)
    print(df)
