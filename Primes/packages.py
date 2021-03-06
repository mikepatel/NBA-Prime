"""
Michael Patel
January 2021

Project description:
    To detect (and predict) an NBA player's prime seasons

File description:
    To import necessary Python packages

"""
################################################################################
# Imports
import os
import re
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from multiprocessing import Pool
import urllib3
from bs4 import BeautifulSoup


################################################################################
# directories
PRIMES_DIR = os.path.join(os.getcwd(), "Primes")
DATA_DIR = os.path.join(PRIMES_DIR, "data")
RESULTS_DIR = os.path.join(PRIMES_DIR, "results")
