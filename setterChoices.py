import pandas as pd
from DataProcessor import DataProcessor as dp
import sys


def main():
    data = pd.read_csv("test.csv", sep=',')

    # make a list of pandas df indexes for each rotation 1-6
    rotIndexes = []
    for i in range(1,7):
        rot = data['rotation'] == i
        rotIndexes.append(rot)

    # parse data for each rotation
    dpList = []
    i = 0
    print("Processing Data")
    for rot in rotIndexes:
        sys.stdout.flush()
        print("{}% Done".format(round(i/6.0, 2)*100), end="\r")
        newDp = dp()
        newDp.parsedata(data[rot])
        dpList.append(newDp)
        i += 1
    i = 0
    print("Creating Plots")
    for d in dpList:
        sys.stdout.flush()
        print("{}% Done".format(round(i/6.0, 2)*100), end="\r")
        d.createPlots()
        i += 1


main()