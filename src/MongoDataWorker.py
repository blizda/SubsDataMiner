import urllib.parse
from abc import ABCMeta
import pymongo
from bson import ObjectId


class MongoWork(metaclass=ABCMeta):
    def __init__(self, login, password, dbName, servDist):
        self.__login = login
        self.__password = password
        self.__dbName = dbName
        self.__servDist = servDist

    def makeConnection(self):
        mongo_uri = "mongodb://" + self.__login + ":" \
                    + urllib.parse.quote(self.__password) \
                    + "@" + self.__servDist \
                    + "/" + self.__dbName
        client = pymongo.MongoClient(mongo_uri)
        db = client[self.__dbName]
        return db


class MongoDataPusher(MongoWork):
    def __init__(self, login, password, dbName, servDist):
        MongoWork.__init__(self, login, password, dbName, servDist)

    def insereSerial(self, serial, db):
        serialDict = {}
        o = ObjectId()
        serialDict['_id'] = o
        serialDict.update(serial.serialInfo)
        db.serials.insert(serialDict)
        for it in serial.seasonsList:
            self.insertSeason(it, db, o)

    def insertSeason(self, season, db, serId):
        seasonDict = {}
        o = ObjectId()
        seasonDict['_id'] = o
        seasonDict['serial_id'] = serId
        seasonDict.update(season.seasInfo)
        db.seasons.insert(seasonDict)
        for it in season.serList:
            self.inserSeria(it, db, serId, o)

    def inserSeria(self, seria, db, serId, seasId):
        seriaDict = {}
        o = ObjectId()
        seriaDict['_id'] = o
        seriaDict['serial_id'] = serId
        seriaDict['season_id'] = seasId
        seriaDict.update(seria.seriaInfo)
        db.serias.insert(seriaDict)

class MongoContrastPusher(MongoWork):
    def __init__(self, login, password, dbName, servDist):
        MongoWork.__init__(self, login, password, dbName, servDist)

    def pushContrastSerialDict(self, contrastDict, db):
        thisContrastDict = {}
        o = ObjectId()
        thisContrastDict['_id'] = o
        thisContrastDict['idf'] = contrastDict
        db.contrast.insert(thisContrastDict)

class MongoDictPush(MongoWork):
    def __init__(self, login, password, dbName, servDist):
        MongoWork.__init__(self, login, password, dbName, servDist)

    def pushDict(self, db, dict):
        thisDict = {}
        o = ObjectId()
        thisDict['_id'] = o
        thisDict['name'] = 'AllWords'
        thisDict['dict'] = dict
        db.dicts.insert(thisDict)

    def pushInversDict(self, db, dict):
        thisDict = {}
        o = ObjectId()
        thisDict['_id'] = o
        thisDict['name'] = 'AllWordsInvers'
        thisDict['dict'] = dict
        db.dicts.insert(thisDict)

    def pushStopWordsDict(self, db, dict):
        thisDict = {}
        o = ObjectId()
        thisDict['_id'] = o
        thisDict['name'] = 'StopWords'
        thisDict['dict'] = dict
        db.dicts.insert(thisDict)

    def pushTopDict(self, db, dict):
        thisDict = {}
        o = ObjectId()
        thisDict['_id'] = o
        thisDict['name'] = 'topDict'
        thisDict['dict'] = dict
        db.dicts.insert(thisDict)

class MongoVectorPusher(MongoWork):
    def __init__(self, login, password, dbName, servDist):
        MongoWork.__init__(self, login, password, dbName, servDist)

    def pushVector(self, db, vector, serialName, serId):
        thisDict = {}
        o = ObjectId()
        thisDict['_id'] = o
        thisDict['SerialName'] = serialName
        thisDict['SerialId'] = serId
        thisDict['vector'] = vector
        db.vectos.insert(thisDict, db)

class MongoCompVactorsPush(MongoWork):
    def __init__(self, login, password, dbName, servDist):
        MongoWork.__init__(self, login, password, dbName, servDist)

    def pushVector(self, db, vector, serialName, serId):
        thisDict = {}
        o = ObjectId()
        thisDict['_id'] = o
        thisDict['SerialName'] = serialName
        thisDict['SerialId'] = serId
        thisDict['vector'] = vector
        db.topvectors.insert(thisDict, db)

class MongoDataPuller(MongoWork):
    def __init__(self, login, password, dbName, servDist):
        MongoWork.__init__(self, login, password, dbName, servDist)

    def findSerial(self, db, qv=None):
        if qv is None:
            cursor = db.serials.find()
        else:
            cursor = db.serials.find(qv)
        resultList = []
        for document in cursor:
            resultList.append(document)
        return resultList

    def findNative(self, db, qv=None):
        if qv is None:
            return db.serials.find()
        else:
            return db.serials.find(qv)

    def takeDict(self, db):
        return db.dicts.find_one({'name': 'AllWords'})

    def takeTopDict(self, db):
        return db.dicts.find_one({'name': 'topDict'})

    def takeInverseDict(self, db):
        return db.dicts.find_one({'name': 'AllWordsInvers'})

    def findVectors(self, db):
        return db.vectos.find()

    def findTopVectors(self, db):
        return db.topvectors.find()

    def pullContrast(self, db):
        return db.contrast.findOne()['idf']
