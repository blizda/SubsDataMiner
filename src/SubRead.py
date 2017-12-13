import re
import math
from abc import ABCMeta
from statistics import median
from chardet import UniversalDetector
from os import listdir
from os.path import join, basename, isdir
from rutermextract import TermExtractor
from GetFitch import GetFitch


class SubsReader:
    def __init__(self, wayToSer):
        self.__listOfTexts = None
        self.__filePath = wayToSer

    def __fileEncoding__(self, filename):
        detector = UniversalDetector()
        with open(filename, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        return detector.result['encoding']

    def __fileInLineReader__(self, filename):
        with open(filename, encoding=self.__fileEncoding__(filename)) as file:
            allLines = ''
            for line in file:
                clearLine = re.sub('<i>|</i>|\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+|\n+|\r+|^\d+', '', line)
                if clearLine:
                    allLines += ' ' + clearLine.replace('{\\an8}', '')
        return allLines

    @property
    def listOfTexts(self):
        if self.__listOfTexts is None:
            self.__listOfTexts = self.__fileInLineReader__(self.__filePath)
        return self.__listOfTexts


class MakeSeria(SubsReader, GetFitch):
    def __init__(self, wayToSer):
        SubsReader.__init__(self, wayToSer)
        GetFitch.__init__(self, self.listOfTexts)
        self.__serName = basename(wayToSer).replace('.srt', '').replace('_', ' ')
        norm = re.sub(r'[^\w\s]+', r' ', self.__serName).strip()
        self.__serName = norm
        self.__allDict = None
        self.__tf = None

    def __str__(self):
        return self.__serName

    def __sortDict__(self, myDict):
        sortDict = {}
        sortDict.update(dict(sorted(myDict.items(), key=lambda x: x[1], reverse=True)))
        return sortDict

    def __tf__(self, text):
        wordDic = {}
        termsQuantity = 0
        term_extractor = TermExtractor()
        for term in term_extractor(text, nested = 'true'):
            termsQuantity += term.count
        for term in term_extractor(text, nested = 'true', weight=lambda term: term.count / termsQuantity):
            norm = re.sub(r'[^\w\s]+', r' ', term.normalized).strip()
            wordDic[norm] = term.count / termsQuantity
        return wordDic

    @property
    def tf(self):
        if self.__tf is None:
            self.__tf = self.__tf__(self.listOfTexts)
        return self.__tf

    @property
    def serName(self):
        return self.__serName

    @property
    def seriaInfo(self):
        allDict = {}
        allDict['seria_name'] = self.serName
        allDict.update(self.fitch)
        allDict['tf'] = self.tf
        return allDict


class MetaSer(metaclass=ABCMeta):
    pass


class MakeSeason:
    def __init__(self, wayToSeason):
        self.__wayToSeason = wayToSeason
        self.__seasName = basename(self.__wayToSeason)
        self.__serList = None
        self.__medFitch = None
        self.__medTf = None
        self.__simpIDF = None

    def __readSerias__(self, wayToSeas):
        serialsList = []
        files = listdir(wayToSeas)
        for file in files:
            if file.endswith('.srt'):
                serialsList.append(MakeSeria(join(wayToSeas, file)))
        return serialsList

    def __seasNotNormaliseIdf__(self, serList):
        korpDic = {}
        for ser in serList:
            term_extractor = TermExtractor()
            temporarDict = {}
            for term in term_extractor(ser.listOfTexts, nested='true'):
                norm = re.sub(r'[^\w\s]+', r' ', term.normalized).strip()
                if norm not in temporarDict:
                    if norm in korpDic:
                        korpDic[norm] = korpDic[norm] + 1
                    else:
                        korpDic[norm] = 1
                    temporarDict[norm] = 1
        for key in korpDic:
            korpDic[key] = korpDic[key]
        return korpDic

    def __medTf__(self, serList):
        medTfDict = {}
        for ser in serList:
            for term in ser.tf:
                if term not in medTfDict:
                    medTfDict[term] = [ser.tf[term]]
                else:
                    medTfDict[term].append(ser.tf[term])
        for it in medTfDict:
            medTfDict[it] = median(medTfDict[it])
        return medTfDict

    def __medFitch__(self, serList):
        medFitch = {}
        for ser in serList:
            for fitch in ser.fitch:
                if fitch not in medFitch:
                    medFitch[fitch] = [ser.fitch[fitch]]
                else:
                    medFitch[fitch].append(ser.fitch[fitch])
        for it in medFitch:
            medFitch[it] = median(medFitch[it])
        return medFitch

    @property
    def serList(self):
        if self.__serList is None:
            self.__serList = self.__readSerias__(self.__wayToSeason)
        return self.__serList

    @property
    def seasName(self):
        return self.__seasName

    @property
    def fitch(self):
        if self.__medFitch is None:
            self.__medFitch = self.__medFitch__(self.serList)
        return self.__medFitch

    @property
    def tf(self):
        if self.__medTf is None:
            self.__medTf = self.__medTf__(self.serList)
        return self.__medTf

    @property
    def idf(self):
        if self.__simpIDF is None:
            self.__simpIDF = self.__seasNotNormaliseIdf__(self.serList)
        return self.__simpIDF

    @property
    def seasLen(self):
        return len(self.serList)

    @property
    def seasInfo(self):
        allDict = {}
        allDict['season_name'] = self.seasName
        allDict.update(self.fitch)
        allDict['tf'] = self.tf
        allDict['idf'] = self.idf
        return allDict


class MakeSerial:
    def __init__(self, wayToSerial):
        self.__wayToSerial = wayToSerial
        self.__serialName = basename(self.__wayToSerial).replace('_', ' ')
        self.__seasList = None
        self.__medFitch = None
        self.__medTf = None
        self.__idf = None
        self.__tfIdf = None

    def __readSeasons__(self, wayToSerial):
        serialsList = []
        files = listdir(wayToSerial)
        for file in files:
            if isdir(join(wayToSerial, file)):
                serialsList.append(MakeSeason(join(wayToSerial, file)))
        return serialsList

    def __idf__(self, seasList):
        korpDic = {}
        serLen = 0
        for seas in seasList:
            serLen += seas.seasLen
            for it in seas.idf:
                if it in korpDic:
                    korpDic[it] = korpDic[it] + seas.idf[it]
                else:
                    korpDic[it] = seas.idf[it]
        for key in korpDic:
            korpDic[key] = math.log2(serLen / korpDic[key])
        return korpDic

    def __medTf__(self, seasList):
        medTfDict = {}
        for season in seasList:
            for term in season.tf:
                if term not in medTfDict:
                    medTfDict[term] = [season.tf[term]]
                else:
                    medTfDict[term].append(season.tf[term])
        for it in medTfDict:
            medTfDict[it] = median(medTfDict[it])
        return medTfDict

    def __medFitch__(self, seasList):
        medFitch = {}
        for season in seasList:
            for fitch in season.fitch:
                if fitch not in medFitch:
                    medFitch[fitch] = [season.fitch[fitch]]
                else:
                    medFitch[fitch].append(season.fitch[fitch])
        for it in medFitch:
            medFitch[it] = median(medFitch[it])
        return medFitch

    def __tfIdf__(self, tf, idf):
        tfIdfDict = {}
        for it in idf:
            tfIdfDict[it] = tf[it] * idf[it]
        return tfIdfDict

    @property
    def seasonsList(self):
        if self.__seasList is None:
            self.__seasList = self.__readSeasons__(self.__wayToSerial)
        return self.__seasList

    @property
    def serialName(self):
        return self.__serialName

    @property
    def fitch(self):
        if self.__medFitch is None:
            self.__medFitch = self.__medFitch__(self.seasonsList)
        return self.__medFitch

    @property
    def tf(self):
        if self.__medTf is None:
            self.__medTf = self.__medTf__(self.seasonsList)
        return self.__medTf

    @property
    def idf(self):
        if self.__idf is None:
            self.__idf = self.__idf__(self.seasonsList)
        return self.__idf

    @property
    def tfIdf(self):
        if self.__tfIdf is None:
            self.__tfIdf = self.__tfIdf__(self.tf, self.idf)
        return self.__tfIdf

    @property
    def serialLen(self):
        return len(self.seasonsList)

    @property
    def serialInfo(self):
        allDict = {}
        allDict['serial_name'] = self.serialName
        allDict.update(self.fitch)
        allDict['tf'] = self.tf
        allDict['idf'] = self.idf
        allDict['tf_idf'] = self.tfIdf
        return allDict
