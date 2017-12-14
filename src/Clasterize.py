from sklearn.preprocessing import StandardScaler
from MongoDataWorker import MongoDataPuller
from numpy import array as ar
from sklearn.cluster import AgglomerativeClustering

mw = MongoDataPuller()
con = mw.makeConnection()
docList = mw.find(con)
dataList = []
nameList = []
for it in docList:
    tempData =[it['redab'], it['adjekt'], it['mestoim'],
               it['substat'], it['quant_first_lex']]
    dataList.append(tempData)
    nameList.append(it['serial_name'])
scaler = StandardScaler()
scaler.fit(ar(dataList).reshape(len(dataList), 5))
X_scaled = scaler.transform(ar(dataList).reshape(len(dataList), 5))
agg = AgglomerativeClustering(n_clusters=2)
lb = agg.fit_predict(X_scaled)
for i in range(len(nameList)):
    print(nameList[i] + " klass " + str(lb[i]))
