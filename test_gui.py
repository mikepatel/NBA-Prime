# IMPORTs
from bs4 import BeautifulSoup
import urllib  # standard library
import csv
import os
import numpy as np
import tkinter as tk

url = "https://www.basketball-reference.com/players/j/jamesle01.html"  # LeBron James

with urllib.request.urlopen(url) as response:
    data = response.read()

soup = BeautifulSoup(data, "html.parser")
print("\n------------------------------------------------------------------------")
player_name = soup.title.text.strip()
player_name, _ = player_name.split("Stats")
player_name = player_name.strip()
print(player_name)


class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("NBA Prime")  # set title of main window
        self.master.configure(background="white")  # set background of main window
        self.master.iconbitmap(os.path.join(os.getcwd(), "res\\hitp_logo_icon.ico"))  # set icon of main window

        self.build_stats_boxes(self.master)  # build group of checkboxes for stat categories

    # build checkbox objects for stat categories
    def build_stats_boxes(self, master):
        self.master = master

        stat_cats = [
            "Points",
            "Rebounds",
            "Assists"
        ]

        for stat in stat_cats:
            cb = tk.Checkbutton(self.master,
                                text=stat,
                                variable=tk.IntVar())
            cb.config(
                background="white"
            )
            cb.pack(anchor=tk.W)


#
root = tk.Tk()
app = Application(root)
root.mainloop()

