

class MapInfo:

    def __init__(self, filename, caption, rotation):
        self.filename = filename
        self.caption = caption
        self.rotation = rotation


class MapInfos:

    def __init__(self):
        self.infos = []

    def getByRotation(self, rotation):
        return [info for info in self.infos if info.rotation == rotation]

    def add(self, info):
        self.infos.append(info)
