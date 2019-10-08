import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


class DataProcessor:

    def __init__(self):
        self.locMap = {}
        self.totatSets = 0.0
        self.rotation = ""

    def parsedata(self, data):
        choices = {
            "BK": 0,
            "Red": 0,
            "C": 0,
            "31": 0,
            "51": 0,
            "61": 0,
            "p": 0
        }

        for index, row in data.iterrows():
            self.rotation = row["rotation"]
            lockey = row["location"]
            choicekey = self.stripDelims(row["choice"])

            if lockey not in self.locMap:
                self.locMap[lockey] = choices.copy()
            self.locMap[lockey][choicekey] += 1

    def showLocPlots(self):
        for items in self.locMap.items():
            loc = items[0]
            p, n = self.createLocationChoiceArray(items[1])
            sets = [["Black", "Middle", "Red"], ["N/A", "Pipe", "C-Ball"]]
            fig, ax = plt.subplots()
            im = ax.imshow(p, cmap = "Greens", vmax=1.0, vmin=0.0)

            ax.set_xticklabels([])
            ax.set_yticklabels([])

            for i in range(2):
                for j in range(3):
                    percent = "{}%".format(p[i][j]*100)
                    text = "{}\n{}\n{} total sets".format(sets[i][j], percent, n[i][j])
                    ax.text(j, i, text, ha="center", va="center", color="black")

            ax.set_title("On passes to location {} in rotation {}".format(loc, self.rotation))
            fig.colorbar(im)
            filename = "Location | {} | {}.png".format(self.rotation, loc)
            fig.savefig(filename)
            plt.close(fig)

    def createLocationChoiceArray(self, m):
        numbers = [[m["BK"], (m["31"] + m["51"] + m["61"]), m["Red"]],
                   [0.0, m["p"], m["C"]]]
        total = sum(numbers[0] + numbers[1])
        total = float(total)
        percent = []
        if total > 0:
            for j in range(2):
                row = []
                for i in range(3):
                    row.append(round(numbers[j][i]/total, 2))
                percent.append(row)
        arr = np.array(percent)

        return arr, numbers

    def stripDelims(self, string):
        string = string.translate(str.maketrans("", "", "(){}<>[]"))
        return string

