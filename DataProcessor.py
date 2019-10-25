import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from SetDataContainer import SetDataContainer as sdc
from MapInfo import MapInfo as mi
from MapInfo import MapInfos

class DataProcessor:

    def __init__(self):
        self.sdc = sdc()
        self.rotation = ""
        self.locMapDirectory = "LocationMaps/"
        self.callMapDirectory = "SetCallMaps/"
        self.ptaMapDirectory = "PTAMaps/"
        self.IMPMAPDirectory = "ImportantTimesMaps/"
        self.sets = [["Black", "Middle", "Red"], ["N/A", "Pipe", "C-Ball"]]
        self.hasPTA = False
        self.hasReset = False
        self.hasIMP = False
        self.lastChoice = ""
        self.locFileInfos = MapInfos()
        self.callFileInfos = MapInfos()
        self.ptaFileInfos = MapInfos()
        self.impFileInfos = MapInfos()


    def parsedata(self, data):
        for index, row in data.iterrows():
            self.rotation = row["rotation"]
            lockey = row["location"]
            choicekey, middleCall = self.stripDelims(row["choice"])
            result = row["result"]
            result1 = result[len(result)-1]
            chosenPlayer = result[:-1]
            passer = row["passer"]
            home, away = row["score"].split("-")
            set = row["set"]
            self.sdc.addToLocMap(lockey, choicekey, result1)
            self.sdc.addToSetCallMap(middleCall, choicekey, result1)
            if int(passer) == int(chosenPlayer):
                self.hasPTA = True
                self.sdc.addToPTAMap(choicekey, result1)
            if self.isImportantTime((int(home), int(away)), int(set)):
                self.hasIMP = True
                self.sdc.addToIMPMAP(choicekey, result)

    def createPlots(self):

        for items in self.sdc.getLocMapItems():
            loc = items[0]
            fig, ax, im, captionString = self.createFigure(items[1])
            ax.set_title("On passes to location {} in rotation {}".format(loc, self.rotation))
            fig.colorbar(im)
            filename = self.locMapDirectory + "Location | {} | {}.png".format(self.rotation, loc)
            # captionString += str(self.rotation) + " : " + loc
            self.locFileInfos.add(mi(filename, captionString, self.rotation))
            fig.savefig(filename)
            plt.close(fig)

        for items in self.sdc.getSetCallMapItems():
            call = items[0]
            fig, ax, im, captionString = self.createFigure(items[1])
            ax.set_title("When the middle is running {} in rotation {}".format(call, self.rotation))
            fig.colorbar(im)
            filename = self.callMapDirectory + "Setter Call | {} | {}.png".format(self.rotation, call)
            # captionString += str(self.rotation) + " : " + call
            self.callFileInfos.add(mi(filename, captionString, self.rotation))
            fig.savefig(filename)
            plt.close(fig)

        if self.hasPTA:
            fig, ax, im, captionString = self.createFigure(self.sdc.ptaMap)
            ax.set_title("On pass to attack in rotation {}".format(self.rotation))
            fig.colorbar(im)
            filename = self.ptaMapDirectory + "PTA | {}.png".format(self.rotation)
            self.ptaFileInfos.add(mi(filename, captionString, self.rotation))
            fig.savefig(filename)
            plt.close(fig)

        if self.hasIMP:
            fig, ax, im, captionString = self.createFigure(self.sdc.IMPMAP)
            ax.set_title("Important time in rotation {}".format(self.rotation))
            fig.colorbar(im)
            filename = self.IMPMAPDirectory + "IMP | {}.png".format(self.rotation)
            self.impFileInfos.add(mi(filename, captionString, self.rotation))
            fig.savefig(filename)
            plt.close(fig)

    def createFigure(self, items):
        p, kp, eff, n, captionString = self.createChoiceArray(items)
        # if p.shape == (0,):
        #     return
        fig, ax = plt.subplots()
        im = ax.imshow(p, cmap="Greens", vmax=1.0, vmin=0.0)

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        for i in range(2):
            for j in range(3):
                percent = "{}%".format(round(p[i][j] * 100, 2))
                kPercent = "{}%".format(round(kp[i][j] * 100, 2))
                efficiency = "{}%".format(round(eff[i][j] * 100, 2))
                text = "{}\n{} of sets\n{} Kill%\n{} Efficiency\n{} total sets".format(self.sets[i][j], percent,
                                                                                       kPercent, efficiency, n[i][j][2])
                ax.text(j, i, text, ha="center", va="center", color="black")
        return fig, ax, im, captionString

    def createChoiceArray(self, m):
        middleStuff = []
        for i in range(3):
            middleStuff.append(m["31"][i] + m["51"][i] + m["61"][i])

        numbers = [[m["BK"], middleStuff, m["Red"]],
                   [[0, 0, 0], m["p"], m["C"]]]
        total = sum([k[2] for k in numbers[0]])
        total += sum([k[2] for k in numbers[1]])
        total = float(total)

        allMids = [m["31"], m["51"], m["61"]]
        stats = []
        for mid in allMids:
            if mid[2] != 0:
                kill = round(mid[0] / mid[2], 2) * 100
                killEff = round((mid[0] - mid[1]) / mid[2], 2) * 100
            else:
                kill = 0.0
                killEff = 0.0
            totalOf = round(mid[2] / total, 2) * 100
            stats.append([kill, killEff, totalOf])

        captionString = "\n"
        sets = ["31", "51", "61"]
        for i in range(len(stats)):
            captionString += "{}: {}% kill, {}% kill efficiency, {}% of total sets\n".format(sets[i], stats[i][0], stats[i][1], stats[i][2])

        percent = []
        killPercent = []
        efficiency = []
        if total > 0:
            for j in range(2):
                row = []
                kpRow = []
                effRow = []
                for i in range(3):
                    kills = numbers[j][i][0]
                    errors = numbers[j][i][1]
                    totalSets = numbers[j][i][2]
                    # percentage of total sets given
                    row.append(totalSets/total)
                    if totalSets == 0:
                        kpRow.append(0.0)
                        effRow.append(0.0)
                    else:
                        # kill percentage
                        kpRow.append(kills/float(totalSets))
                        # kill efficiency
                        effRow.append((kills-errors) / float(totalSets))

                percent.append(row)
                killPercent.append(kpRow)
                efficiency.append(effRow)
        arr = np.array(percent)
        kpArr = np.array(killPercent)
        effArr = np.array(efficiency)

        return arr, kpArr, effArr, numbers, captionString

    def stripDelims(self, string):
        actualCall = "None"
        middleCall = string[0]
        middleRuns = ["31", "51", "61"]
        if middleCall == "(":
            actualCall = "51"
        elif middleCall == "[":
            actualCall = "31"
        elif middleCall == "<":
            actualCall = "61"
        elif string in middleRuns:
            actualCall = string

        string = string.translate(str.maketrans("", "", "(){}<>[]"))
        return string, actualCall

    def getCaptions(self):
        return self.locFileInfos, self.callFileInfos, self.ptaFileInfos, self.impFileInfos

    def isImportantTime(self, score, gameSet):
        if gameSet < 5:
            return (score[0] >= 20 or score[1] >= 20) and abs(score[0] - score[1]) <= 2
        else:
            return (score[0] >= 10 or score[1] >= 10) and abs(score[0] - score[1]) <= 2


