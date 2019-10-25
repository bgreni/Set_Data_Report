import pandas as pd
from DataProcessor import DataProcessor as dp
from PdfGenerator import PdfGenerator as pdfg
import sys
from MapInfo import MapInfos


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
    locCaptions = MapInfos()
    callCaptions = MapInfos()
    ptaCaptions = MapInfos()
    impCaptions = MapInfos()
    print("Creating Plots")
    for d in dpList:
        sys.stdout.flush()
        # print("{}% Done".format(round(i/6.0, 2)*100), end="\r")
        d.createPlots()
        i += 1
        captions = d.getCaptions()
        locCaptions.infos += captions[0].infos
        callCaptions.infos += captions[1].infos
        ptaCaptions.infos += captions[2].infos
        impCaptions.infos += captions[3].infos

    pdfGen = pdfg()
    pdfGen.createPdf([locCaptions, callCaptions, ptaCaptions, impCaptions])


main()