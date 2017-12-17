import copy

from MongoDataWorker import MongoDataPuller


class MakeVectors:
    def __init__(self, login, password, dbName, servDist):
        mw = MongoDataPuller(login, password, dbName, servDist)
        con = mw.makeConnection()
        self.cursor = mw.findNative(con)
        self.dictT = mw.takeTopDict(con)

    def makeVectors(self):
        vectList = []
        nameList = []
        vec = [0 for i in range(1000)]
        for document in self.cursor:
            a = copy.copy(vec)
            nameList.append(document['serial_name'])
            m = document['tf_idf']
            for it in self.dictT:
                if it in m:
                    a[self.dictT[it]] = m[it] * 100
            vectList.append(a)
        return vectList, nameList
