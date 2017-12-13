import urllib.parse

import os
import pymongo
from MongoDataWorker import MongoDataPusher, MongoDataPuller
from SubRead import *

#testSer = MakeSeria('../out/Серия_15.srt')
#testSer2 = MakeSeria('../out/Серия_3.srt')
#print(testSer.allSerInfo)
#print(testSer2.allSerInfo)
#testSeas = MakeSeason('../out')
#print(testSeas.seasInfo)
#client = pymongo.MongoClient("mongodb://blizda:USS17@01Vankosr@185.40.31.63/test_serial") # defaults to port 27017
#mongo_uri = "mongodb://blizda:" + urllib.parse.quote("USS17@01Vankosr") + "@185.40.31.63/test_serial"
#client = pymongo.MongoClient(mongo_uri)
#db = client.test_serial
#db.serials.insert(MakeSerial('../out/Game_of_Thrones').serialInfo)
# print the number of documents in a collection
#print(db.test_serial.count())
#testSer = MakeSerial('../out/Game_of_Thrones')
#print(testSer.serialInfo)cursor = db.serials.find(qv)
#serial = MakeSerial('../out/Mr_Robot')
#mw = MongoDataPusher('blizda', 'USS17@01Vankosr', 'test_serial', '185.40.31.63')
#con = mw.makeConnection()
#print("ok")
#kk = '../out'
