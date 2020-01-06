

class SetDataContainer:

    def __init__(self):
        self.locMap = {}
        self.setCallMap = {}
        self.ptaMap = self.getChoices()
        self.IMPMAP = self.getChoices()
        self.posResetMap = self.getChoices()
        self.negResetMap = self.getChoices()
        self.runBreakMap = self.getChoices()
        self.playerToPos = {}
        self.passCounts = {}

    def addToLocMap(self, lockey, choicekey, result):
        if lockey not in self.locMap:
            self.locMap[lockey] = self.getChoices()
        self.addToNestedMap(self.locMap, choicekey, result, lockey)

    def addToSetCallMap(self, callkey, choicekey, result):
        if callkey not in self.setCallMap:
            self.setCallMap[callkey] = self.getChoices()
        self.addToNestedMap(self.setCallMap, choicekey, result, callkey)

    def addToPTAMap(self, choicekey, result):
        self.addToMap(self.ptaMap, choicekey, result)
        self.ptaMap[choicekey][3] += 1

    def addToIMPMAP(self, choicekey, result):
        self.addToMap(self.IMPMAP, choicekey, result)

    def addToPosResetMap(self, choicekey, result):
        self.addToMap(self.posResetMap, choicekey, result)

    def addToNegResetMap(self, choicekey, result):
        self.addToMap(self.negResetMap, choicekey, result)

    def addToRunBreakMap(self, choicekey, result):
        self.addToMap(self.runBreakMap, choicekey, result)

    def addToMap(self, m, choicekey, result):
        m[choicekey][2] += 1
        if result == "K":
            m[choicekey][0] += 1
        elif result == "E":
            m[choicekey][1] += 1

    def addPass(self, player):
        if player not in self.passCounts:
            self.passCounts[player] = 0
        self.passCounts[player] += 1

    def addPasses(self, posMap):
        for player, count in self.passCounts.items():
            if player in posMap and player != -1:
                pos = posMap[player]
                self.ptaMap[pos][3] += count


    def addToNestedMap(self, m, choicekey, result, extraIndex):
        m[extraIndex][choicekey][2] += 1
        if result == "K":
            m[extraIndex][choicekey][0] += 1
        elif result == "E":
            m[extraIndex][choicekey][1] += 1

    def getLocMapItems(self):
        return self.locMap.items()

    def getSetCallMapItems(self):
        return self.setCallMap.items()

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
            "p": self.initSetInformation(),
            "D": self.initSetInformation(),
            "FS": self.initSetInformation(),
            "62": self.initSetInformation()
        }
        return choices

    def initSetInformation(self):
        return [0.0, 0.0, 0, 0]