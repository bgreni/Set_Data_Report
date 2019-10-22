

class SetDataContainer:

    def __init__(self):
        self.locMap = {}
        self.setCallMap = {}
        self.ptaMap = self.getChoices()
        self.resetMap = self.getChoices()
        self.IMPMAP = self.getChoices()

    def addToLocMap(self, lockey, choicekey, result):
        if lockey not in self.locMap:
            self.locMap[lockey] = self.getChoices()
        self.locMap[lockey][choicekey][2] += 1
        if result == "K":
            self.locMap[lockey][choicekey][0] += 1
        elif result == "E":
            self.locMap[lockey][choicekey][1] += 1

    def addToSetCallMap(self, callkey, choicekey, result):
        if callkey not in self.setCallMap:
            self.setCallMap[callkey] = self.getChoices()
        self.setCallMap[callkey][choicekey][2] += 1
        if result == "K":
            self.setCallMap[callkey][choicekey][0] += 1
        elif result == "E":
            self.setCallMap[callkey][choicekey][1] += 1

    def addToPTAMap(self, choicekey, result):
        self.ptaMap[choicekey][2] += 1
        if result == "K":
            self.ptaMap[choicekey][0] += 1
        elif result == "E":
            self.ptaMap[choicekey][1] += 1

    def addToResetmap(self, choicekey, result):
        self.resetMap[choicekey][2] += 1
        if result == "K":
            self.resetMap[choicekey][0] += 1
        elif result == "E":
            self.resetMap[choicekey][1] += 1

    def addToIMPMAP(self, choicekey, result):
        self.IMPMAP[choicekey][2] += 1
        if result == "K":
            self.IMPMAP[choicekey][0] += 1
        elif result == "E":
            self.IMPMAP[choicekey][1] += 1

    def getLocMapItems(self):
        return self.locMap.items()

    def getSetCallMapItems(self):
        return self.setCallMap.items()

    def getResetMapItems(self):
        return self.resetMap.items()

    def getIMPMAPItems(self):
        return self.IMPMAP.items()

    def getChoices(self):
        choices = {
            "BK": self.initSetInformation(),
            "Red": self.initSetInformation(),
            "C": self.initSetInformation(),
            "31": self.initSetInformation(),
            "51": self.initSetInformation(),
            "61": self.initSetInformation(),
            "p": self.initSetInformation()
        }
        return choices

    def initSetInformation(self):
        return [0.0, 0.0, 0.0]