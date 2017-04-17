import os

import unicodedata
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
    speak_list = []
    speak_list.append(appName.split('.')[0].lower())
    if checkAPP(path):
        pref["path"] = path
        pref["appNome"] = speak_list
        pref["fala"] = appName
        pref["_id"] = uuid.uuid1()
        sysProgram.insert(pref)
    else:
        pass


def printDocApp():
     for doc in db.sysProgram.find():
        print(doc)

def findDocApp(app_name):
    for doc in db.sysProgram.find():
        if app_name in doc['appNome']:
            print 'q'
    # doc = db.sysProgram.find_one({"appNome": app_name})
    # if (doc == None):
    #     return None
    # else:
    #     return doc

def removeDocApp(path):
    db.sysProgram.delete_many({"path":path})

def returnDocApp(appName):
     for doc in db.sysProgram.find({"appNome":appName}):
         print (doc["path"])
         return doc["path"], doc["appNome"]
     return ("Program not found")

def returnAllDocApp():
    return db.sysProgram.find()

def updateDocApp(appName, info):
    doc = findDocApp(appName)
    print doc
    speak_list = doc['appNome']
    print type(speak_list)
    print speak_list
    if info in speak_list:
        return 'Nickname already exist.'
    else:
        print type(appName)
        print type(info)
        speak_list.append(info)
        # db.ProductData.update_one({
        #       '_id': doc['_id']
        #     },{
        #       '$set': {
        #         'fala': speak_list
        #       }
        #     }, upsert=False)
        return 'Nickname added.'

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

def removeProfile():
    db.userProfile.delete_many({})

def addProfile(user, callname):
    pref = {}
    print user, callname
    if checkUser(user):
        pref["user"] = user
        pref["callname"] = callname
        pref["_id"] = uuid.uuid1()
        userProfile.insert(pref)
    else:
        print ('Error - Not able to insert user')
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