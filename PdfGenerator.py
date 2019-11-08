from pylatex import Document, Section, Figure, SubFigure, Command, Subsection, Package, NoEscape


class PdfGenerator:

    def __init__(self, directory, name):
        geometry_options = {"right": "1cm", "left": "1cm", "top": "1cm", "bottom": "1cm"}
        self.doc = Document("{}/{}-Report".format(directory, name), geometry_options=geometry_options)
        self.doc.documentclass = Command(
            'documentclass',
            options=['10pt', 'vertical'],
            arguments=['article'],
        )
        self.doc.preamble.append(Command("title", name))
        self.doc.real_data.append(Command("date", ""))
        self.doc.append(NoEscape(r'\maketitle'))
        self.doc.packages.append(Package("placeins"))
        self.locMapDirectory = "LocationMaps/"
        self.callMapDirectory = "SetCallMaps/"
        self.ptaMapDirectory = "PTAMaps/"
        self.IMPMAPDirectory = "ImportantTimesMaps/"

    def createPdf(self, mapInfosList):
        self.createLocSection(mapInfosList[0])
        self.createCallSection(mapInfosList[1])
        self.createPtaSection(mapInfosList[2])
        self.createImpSection(mapInfosList[3])
        self.createPosResetSection(mapInfosList[4])
        self.createNegResetSection(mapInfosList[5])
        self.createRunBreakSection(mapInfosList[6])
        self.createAllRotationsSection(mapInfosList)
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

    def createPosResetSection(self, posResetInfos):
        section = Section("Positive Reset Maps")
        self.generateSection(section, posResetInfos)

    def createNegResetSection(self, negResetInfos):
        section = Section("Negative Reset Maps")
        self.generateSection(section, negResetInfos)

    def createRunBreakSection(self, runBreakInfos):
        section = Section("Run Breaking Decision Maps")
        self.generateSection(section, runBreakInfos)

    def createAllRotationsSection(self, allInfos):
        section = Section("All Rotations")
        locSub = Subsection("Pass Location")
        self.generateAllRotationSubsection(allInfos[0], locSub, section)
        callSub = Subsection("Setter Call")
        self.generateAllRotationSubsection(allInfos[1], callSub, section)
        ptaSub = Subsection("Pass To Attack")
        self.generateAllRotationSubsection(allInfos[2], ptaSub, section)
        impSub = Subsection("Important Times")
        self.generateAllRotationSubsection(allInfos[3], impSub, section)
        posSub = Subsection("Positive Reset")
        self.generateAllRotationSubsection(allInfos[4], posSub, section)
        negSub = Subsection("Negative Reset")
        self.generateAllRotationSubsection(allInfos[5], negSub, section)
        runBSub = Subsection("Run Break")
        self.generateAllRotationSubsection(allInfos[6], runBSub, section)
        self.doc.append(section)


    def generateAllRotationSubsection(self, infos, subsection, section):
        subInfos = infos.getByRotation("All Rotations")
        if len(subInfos) != 0:
            self.makeImages(subsection, subInfos)
            section.append(subsection)
            section.append(Command("FloatBarrier"))

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
        self.doc.generate_pdf(clean_tex=True, compiler='pdflatex')
