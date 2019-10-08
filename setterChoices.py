import pandas as pd
from DataProcessor import DataProcessor as dp

def main():
    data = pd.read_csv("test.csv", sep=',')

    # make a list of pandas df indexes for each rotation 1-6
    rotIndexes = []
    for i in range(1,7):
        rot = data['rotation'] == i
        rotIndexes.append(rot)

    # parse data for each rotation
    dpList = []
    for rot in rotIndexes:
        newDp = dp()
        newDp.parsedata(data[rot])
        dpList.append(newDp)
    for d in dpList:
        d.showLocPlots()


main()