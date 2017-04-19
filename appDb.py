import os

import unicodedata
from pymongo import MongoClient
import uuid
import difflib

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
    doc_list = []
    for doc in db.sysProgram.find():
        if app_name in doc['appNome']:
            seq = difflib.SequenceMatcher(None, doc['appNome'], app_name)
            match_value=seq.ratio()
            if match_value >= 0.8:
                return doc["path"], doc["appNome"], 'open'
            else:
                doc_list.append({"doc":doc,"match_value":match_value})
    if len(doc_list) > 0:
        doc_list_final = sorted(doc_list, key=lambda k: k['match_value'],reverse=True)
        print doc_list_final[0]['doc']
        return doc_list_final[0]['doc']["path"],doc_list_final[0]['doc']["appNome"], 'ask'
    else:
        return ("Program not found")

def removeDocApp(path):
    db.sysProgram.delete_many({"path":path})

def returnDocApp(appName):
     for doc in db.sysProgram.find({"appNome":appName}):
         return doc["path"], doc["appNome"]
     return ("Program not found")

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

def removeProfile():
    db.userProfile.delete_many({})

def addProfile(user, callname):
    pref = {}
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
        return doc
     return ("Error")