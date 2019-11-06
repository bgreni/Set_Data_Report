

class ResetTracker:

    def __init__(self):
        self.lastHitter = ""
        self.currentHitter = ""
        self.lastResult = ""
        self.lastHitSet = ""
        self.currentHitSet = ""

    def isPosReset(self):
        return self.sameHitter() and self.isPosResult() and self.sameSet()

    def isNegReset(self):
        return self.sameHitter() and self.isNegResult() and self.sameSet()

    def sameHitter(self):
        return self.lastHitter == self.currentHitter

    def isPosResult(self):
        return self.lastResult == "K" or self.lastResult == "C"

    def isNegResult(self):
        return self.lastResult == "E"

    def sameSet(self):
        return self.lastHitSet == self.currentHitSet

    def updateOld(self, hitResult):
        self.lastHitter = self.currentHitter
        self.lastResult = hitResult
        self.lastHitSet = self.currentHitSet