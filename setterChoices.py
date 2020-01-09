import pandas as pd
from DataProcessor import DataProcessor as dp
from PdfGenerator import PdfGenerator as pdfg
from MapInfo import MapInfos
from multiprocessing import Queue, Process
import tkinter as tk
from tkinter import filedialog



class SetterChoicesReport:
    """Generates a report of heat maps for various cases"""

    def __init__(self, totalPTAMap=None, allptaByRotation=None):
        locInfos = MapInfos()
        callInfos = MapInfos()
        ptaInfos = MapInfos()
        impInfos = MapInfos()
        posResetInfos = MapInfos()
        negResetInfos = MapInfos()
        runBreakInfos = MapInfos()
        if totalPTAMap is None:
            self.givenPTA = True
            self.totalPTAMap = dp().sdc.getChoices()
        else:
            self.totalPTAMap = totalPTAMap
            self.givenPTA = False
        self.allInfos = [locInfos, callInfos, ptaInfos,
                         impInfos, posResetInfos, negResetInfos, runBreakInfos]
        self.givenData = False
        self.ptaByRotation = {}
        self.allptaByRotation = allptaByRotation

    def getFileName(self):
        """Lets the user chose a file, then returns the name of that file and the path to it"""
        root = tk.Tk()
        root.withdraw()
        # opens finder window to pick a file
        fullPath = filedialog.askopenfilename()
        pathList = fullPath.split("/")
        filename = pathList.pop()
        pathNoFn = "/".join(pathList)

        return filename, pathNoFn

    def run(self, filename, path, given=None):
        """Runs the whole process, from parsing the csv,
            to generating the plots, then putting them into
            a pdf report"""

        if not self.givenData:
            try:
                data = pd.read_csv("{}/{}".format(path, filename), sep=',')
            except:
                raise IOError("could not read from file: {}".format(filename))
        else:
            data = given

        # make a list of pandas df indexes for each rotation 1-6
        rotIndexes = []
        for i in range(1, 7):
            rot = data['rotation'] == i
            rotIndexes.append(rot)

        # parse data for each rotation
        dpList = []
        print("Processing Data")
        for rot in rotIndexes:
            posMap = self.inferPositions(data[rot])
            newDp = dp(path, posMap)
            newDp.parsedata(data[rot])
            dpList.append(newDp)

        print("Creating Plots")
        for d in dpList:
            d.createPlots()
            # add infos to total
            infos = d.getInfos()
            for i in range(len(self.allInfos)):
                self.allInfos[i].infos += infos[i].infos

        # generate the pdf
        pdfGen = pdfg(path, filename.split(".")[0])
        pdfGen.createPdf(self.allInfos)

    def threadFunction(self, queue, rot, data, path, allRot, posMap, allPTAInfos=None, ptaQ=None):
        """Function passed to the processes when running in threaded mode"""

        newDp = dp(path, posMap)
        if allRot:
            newDp.parsedata(data, "All Rotations", passedPTAMap=allPTAInfos)
        else:
            newDp.parsedata(data[rot])
            if allPTAInfos is None:
                ptaQ.put((newDp.sdc.ptaMap, newDp.hasPTA, newDp.rotation))
            else:
                rotation = str(newDp.rotation)
                ptaQ.put((allPTAInfos[rotation], True, rotation))
                newDp.sdc.ptaMap = allPTAInfos[rotation]
        newDp.createPlots()
        infos = newDp.getInfos()
        queue.put(infos)


    def runThreaded(self, filename, path, given=None):
        """Same as the run() method, but splits the creation of each rotations maps into
            seperate processes"""

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
        ptaQ = Queue()
        print("Processing Data")
        for rot in rotIndexes:
            posMap = self.inferPositions(data[rot])
            if self.allptaByRotation is None:
                p = Process(target=self.threadFunction, args=[q, rot, data, path, False, posMap, None, ptaQ])
            else:
                p = Process(target=self.threadFunction, args=[q, rot, data, path, False, posMap, self.allptaByRotation, ptaQ])
            p.start()
            threads.append(p)

        for p in threads:
            infos = q.get()
            ptamap, hasPTA, rotation = ptaQ.get()
            if hasPTA:
                self.combineMaps(ptamap, rotation, self.totalPTAMap)
            for i in range(len(self.allInfos)):
                self.allInfos[i].infos += infos[i].infos

        for thread in threads:
            thread.join()

        # start one for all rotations
        posMap = self.inferPositions(data)
        p = Process(target=self.threadFunction, args=[q, None, data, path, True, posMap, self.totalPTAMap, None])
        p.start()
        infos = q.get()
        for i in range(len(self.allInfos)):
            self.allInfos[i].infos += infos[i].infos

        p.join()
        pdfGen = pdfg(path, filename.split(".")[0])
        pdfGen.createPdf(self.allInfos)

    def inferPositions(self, data):
        countMap = {}
        for index, row in data.iterrows():
            set = dp.stripDelims(row["choice"])[0]
            player = row["result"][:-1]
            if player not in countMap:
                countMap[player] = {}
            if set not in countMap[player]:
                countMap[player][set] = 0
            countMap[player][set] += 1

        posInferenceMap = {}
        for p, s in countMap.items():
            pos = max(s)
            posInferenceMap[p] = pos
        return posInferenceMap

    def combineMaps(self, map2, rotation, map1):
        for key in map1.keys():
            for i in range(len(map1[key])):
                map1[key][i] += map2[key][i]

        self.ptaByRotation[rotation] = map2


