import pandas as pd
import numpy as np
from DataProcessor import DataProcessor as dp
from PdfGenerator import PdfGenerator as pdfg
import sys
from MapInfo import MapInfos
import time
import multiprocessing
from multiprocessing import Queue, Process
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

class SetterChoicesReport:

    def __init__(self):
        locInfos = MapInfos()
        callInfos = MapInfos()
        ptaInfos = MapInfos()
        impInfos = MapInfos()
        posResetInfos = MapInfos()
        negResetInfos = MapInfos()
        runBreakInfos = MapInfos()
        self.allInfos = [locInfos, callInfos, ptaInfos,
                         impInfos, posResetInfos, negResetInfos, runBreakInfos]
        self.lock = multiprocessing.Lock()
        self.givenData = False

    def getFileName(self):
        fullPath = filedialog.askopenfilename()
        pathList = fullPath.split("/")
        filename = pathList.pop()
        pathNoFn = "/".join(pathList)

        return filename, pathNoFn

    def run(self, filename, path, given=None):
        totalTime = time.time()
        start_time = time.time()
        if not self.givenData:
            data = pd.read_csv("{}/{}".format(path, filename), sep=',')
        else:
            data = given
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
            # print("{}% Done".format(round(i/6.0, 2)*100), end="\r")
            newDp = dp(path)
            newDp.parsedata(data[rot])
            dpList.append(newDp)
            i += 1
        # print("finished parsing data in {} seconds".format(round(time.time() - start_time, 3)))
        start_time = time.time()
        i = 0
        print("Creating Plots")
        for d in dpList:
            # sys.stdout.flush()
            # print("{}% Done".format(round(i/6.0, 2)*100), end="\r")
            d.createPlots()
            i += 1
            captions = d.getCaptions()
            for i in range(len(self.allInfos)):
                self.allInfos[i].infos += captions[i].infos
        # print("finished create plots in {} seconds".format(round(time.time() - start_time, 3)))
        start_time = time.time()
        pdfGen = pdfg(path, filename.split(".")[0])
        pdfGen.createPdf(self.allInfos)
        # print("finished creating pdf in {} seconds".format(round(time.time() - start_time, 3)))
        # print("Total time: {} seconds".format(round(time.time() - totalTime, 3)))

    def threadFunction(self, queue, rot, data, path):
        newDp = dp(path)
        newDp.parsedata(data[rot])
        newDp.createPlots()
        captions = newDp.getCaptions()
        queue.put(captions)


    def runThreaded(self, filename, path, given=None):
        totalTime = time.time()
        start_time = time.time()
        if not self.givenData:
            data = pd.read_csv("{}/{}".format(path, filename), sep=',')
        else:
            data = given

        # make a list of pandas df indexes for each rotation 1-6
        rotIndexes = []
        for i in range(1, 7):
            rot = (data['rotation'] == i)
            rotIndexes.append(rot)

        threads = []
        q = Queue()
        print("Processing Data")
        for rot in rotIndexes:
            p = Process(target=self.threadFunction, args=[q, rot, data, path])
            p.start()
            threads.append(p)

        for p in threads:
            captions = q.get()
            for i in range(len(self.allInfos)):
                self.allInfos[i].infos += captions[i].infos

        # print("finished create plots in {} seconds".format(round(time.time() - start_time, 3)))
        start_time = time.time()
        for thread in threads:
            thread.join()

        pdfGen = pdfg(path, filename.split(".")[0])
        pdfGen.createPdf(self.allInfos)
        # print("finished creating pdf in {} seconds".format(round(time.time() - start_time, 3)))
        # print("Total time: {} seconds".format(round(time.time() - totalTime, 3)))
