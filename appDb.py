import os
from pymongo import MongoClient
import uuid

client = MongoClient()

db = client['TaskAuto']
sysProgram = db["sysProgram"]
userProfile = db["userProfile"]


def checkAPP(path):
    if (db.sysProgram.find_one({"path": path}) == None):
        return True
    else:
        return False

def insereDocApp(path, appName):
    pref = {}
    if checkAPP(path):
        pref["path"] = path
        pref["appNome"] = appName
        pref["fala"] = appName
        pref["_id"] = uuid.uuid1()
        sysProgram.insert(pref)
    else:
        pass
        # print("Not able to insert")

def printDocApp():
     for doc in db.sysProgram.find():
        print(doc)

def removeDocApp(path):
    db.sysProgram.delete_many({"path":path})

def returnDocApp(appName):
     for doc in db.sysProgram.find({"appNome":appName}):
         print (doc["path"])
         return doc["path"], doc["appNome"]
     return ("Comando nao existente")

def returnAllDocApp():
    return db.sysProgram.find()

def startDB():
    directory = '/Applications'

    for filename in os.listdir(directory):
        # print filename

        if filename.endswith(".app"):
            # print(os.path.join(directory, filename))

            if checkAPP(filename) is True:
                insereDocApp((os.path.join(directory, filename)), filename)

    print ("Ready to be used.")

def checkUser(user):
    if (db.userProfile.find_one({"user": user}) == None):
        return True
    else:
        return False

def addProfile(user, callname):
    pref = {}
    print user, callname
    if checkUser(user):
        pref["user"] = user
        pref["callname"] = callname
        pref["_id"] = uuid.uuid1()
        userProfile.insert(pref)
    else:
        print ('aqui')
        pass

def returnAllDocUser():
    return db.userProfile.find()

def printDocUser():
     for doc in db.userProfile.find():
        print(doc)

def returnDocUser():
     for doc in db.userProfile.find():
        print(doc)
        return doc
     return ("Error")

