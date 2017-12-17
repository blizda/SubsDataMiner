from MongoDataWorker import MongoDataPuller
from statistics import median

class MakeDict:
    def __init__(self, login, password, dbName, servDist):
        mw = MongoDataPuller(login, password, dbName, servDist)
        con = mw.makeConnection()
        self.docList = mw.findSerial(con)
        self.dicForBags = None
        self.invertdicForBags = None

    def reduceDict(self, myDict, lentop, lenDict):
        return dict(sorted(myDict.items(), key=lambda x: x[1], reverse=True)[lentop:lenDict])

    def makeDicts(self):
        allDict = {}
        tDict = {}
        numDict = {}
        i = 0
        for it in self.docList:
            allDict.update(it['tf_idf'])
        for it in allDict:
            tDict[it] = i
            numDict[str(i)] = it
            i += 1
        return tDict, numDict

    def makeTopDict(self):
        allDict = {}
        for it in self.docList:
            for kit in it['idf']:
                if kit in allDict:
                    allDict[kit] = allDict[kit] + it['idf'][kit]
                else:
                    allDict[kit] = it['idf'][kit]
        allDict = self.reduceDict(allDict, 3000, 4000)
        i = 0
        for it in allDict:
            allDict[it] = i
            i = i + 1
        return allDict

    def makeTopIdf(self):
        allDict = {}
        for it in self.docList:
            for kit in it['idf']:
                if kit in allDict:
                    allDict[kit].append(it['tf_idf'][kit])
                else:
                    temList = []
                    temList.append(it['tf_idf'][kit])
                    allDict[kit] = temList
        for it in allDict:
            allDict[it] = median(allDict[it])
        allDict = self.reduceDict(allDict, 3000, 4000)
        i = 0
        for it in allDict:
            allDict[it] = i
            i = i + 1
        return allDict