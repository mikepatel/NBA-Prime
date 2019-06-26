import numpy as np

ppg = [
    2,
    5,
    7,
    4,
    9,
    4,
    5,
    2,
    8,
    7
]

slide_window = 3
for i in range(len(ppg)-slide_window+1):
    print("\n")
    print(ppg[i: i+slide_window])
    print(np.mean(ppg[i: i+slide_window]))