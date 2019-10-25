from pylatex import Document, Section, Figure, NoEscape, MiniPage, VerticalSpace, LineBreak, SubFigure, Tabular, Command, NewPage, Subsection, Package
from os import listdir


class PdfGenerator:

    def __init__(self):
        geometry_options = {"right": "1cm", "left": "1cm", "top": "1cm", "bottom": "1cm"}
        self.doc = Document("Report", geometry_options=geometry_options)
        self.doc.documentclass = Command(
            'documentclass',
            options=['10pt', 'vertical'],
            arguments=['article'],
        )
        self.doc.packages.append(Package("placeins"))
        self.locMapDirectory = "LocationMaps/"
        self.callMapDirectory = "SetCallMaps/"
        self.ptaMapDirectory = "PTAMaps/"
        self.IMPMAPDirectory = "ImportantTimesMaps/"

    def createPdf(self, mapInfosList):
        self.createLocSection(mapInfosList[0])
        # self.doc.append(Command("clearpage"))
        self.createCallSection(mapInfosList[1])
        # self.doc.append(Command("clearpage"))
        self.createPtaSection(mapInfosList[2])
        self.createImpSection(mapInfosList[3])
        self.finish()

    def generateSection(self, section, fileInfos):
        for i in range(1, 7):
            sub = Subsection("Rotation {}".format(i))
            subInfos = fileInfos.getByRotation(i)
            lenSub = len(subInfos)
            if lenSub != 0:
                self.makeImages(sub, subInfos)
                section.append(sub)
                section.append(Command("FloatBarrier"))
        self.doc.append(section)

    def createLocSection(self, locFileInfos):
        section = Section("Pass Location Maps")
        self.generateSection(section, locFileInfos)

    def createCallSection(self, callFileInfos):
        section = Section("Setter Call Maps")
        self.generateSection(section, callFileInfos)

    def createPtaSection(self, ptaFileInfos):
        section = Section("Pass to Attack Maps")
        self.generateSection(section, ptaFileInfos)

    def createImpSection(self, impFileInfos):
        section = Section("Important Times Maps")
        self.generateSection(section, impFileInfos)

    def makeImages(self, section, fileInfos):
        figure = Figure(position="h")
        for index, infos in enumerate(fileInfos):
            image = self.createImage(infos.filename, infos.caption)
            figure.append(image)
            if index % 2 == 1:
                section.append(figure)
                figure = Figure(position="h")
            if index == len(fileInfos) - 1:
                section.append(figure)


    def createImage(self, filename, captionString):
        fig = SubFigure(position="h")
        file, typ = filename.split(".")
        fig.add_image("\"{}\".{}".format(file, typ), width="240px")
        fig.add_caption(captionString)
        return fig

    def finish(self):
        self.doc.generate_pdf(clean_tex=False, compiler='pdflatex')
