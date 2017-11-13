import urllib.parse
import pymongo
from bson import ObjectId


class MongoWorker:
    def __init__(self, login, password, dbName, serwDist):
        self.__login = login
        self.__password = password
        self.__dbName = dbName
        self.__serwDist = serwDist

    def makeConnection(self):
        mongo_uri = "mongodb://" + self.__login + ":" +\
                    urllib.parse.quote(self.__password) + "@" + self.__serwDist + "/" + self.__dbName
        client = pymongo.MongoClient(mongo_uri)
        db = client[self.__dbName]
        return db

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

class MongoDataGetter:
    def __init__(self):
        pass

