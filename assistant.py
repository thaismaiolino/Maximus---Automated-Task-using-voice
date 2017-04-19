from datetime import datetime
import speech_recognition as sr
import webbrowser
import unicodedata
import appDb as db
import os
import requests
import urllib2
import time

global start_listening
start_listening = False
global nickname
global wait_anwser
global user
user = db.returnDocUser()['user']
wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

def doAction(a):
    global start_listening
    global wait_anwser
    if nickname in a:
        action = a.replace(nickname, "").lstrip(' ')
        systemTalks("Hi" + user)
        if a == "hey dude":
            systemTalks("How can I help you?")
        else:
            systemTalks("wait a sec.")
    else:
        action = a


    if wait_anwser['active'] == True and wait_anwser["waiting_command"] == True:
        if "open" in action.lower(): # or "run" in action.lower() or "reopen" in action.lower():
            if "facebook" in action.lower():
                url = 'https://www.facebook.com/'
                webbrowser.open(url, new=0, autoraise=True)
                systemTalks("Done. Need something else?")
                wait_anwser = {"active": True, "waiting_command": False, "waiting_anwser":True, "action":None, "program": None}

            else:
                program = action.replace("open", "").lstrip(' ')
                print program
                tmp = db.findDocApp(program)
                # tmp = db.returnDocApp(program)
                if tmp == "Program not found":
                   systemTalks("You do not have "+program+". Would you like to download it?")
                   wait_anwser = {"active": True,"waiting_command": False, "waiting_anwser":True ,"action":"download", "program": program}

                else:
                    if tmp[2] == 'open':
                        path_ini = tmp[0].replace(' ', '\ ')
                        path_tmp = path_ini.split('/')
                        path = "/"+path_tmp[1]+"/"+path_tmp[2]+"/Contents/MacOS/" + path_tmp[2].replace('.app','')
                        os.system(path)
                        wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}
                    else:
                        path_ini = tmp[0].replace(' ', '\ ')
                        path_tmp = path_ini.split('/')
                        path = "/"+path_tmp[1]+"/"+path_tmp[2]+"/Contents/MacOS/" + path_tmp[2].replace('.app','')
                        systemTalks('It looks like that you do not have '+program+'. But you have '+tmp[1]+'. Would you like to open it?')
                        wait_anwser = {"active": True,"waiting_command": False, "waiting_anwser":True ,"action":"open", "program": path}


        elif "search" in action.lower():
            url = 'https://www.google.com.br/#q=' + unicodedata.normalize('NFKD', action.replace("search", "").lstrip(' ')
                                                                .replace(" ", "+")).encode('ascii','ignore')
            webbrowser.open(url, new=0, autoraise=True)

            wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

        elif "install" in action.lower():
            url = 'http://www.google.com/search?hl=en&q='+unicodedata.normalize('NFKD', action.replace("install", "")
                    .lstrip(' ').replace(" ", "+")).encode('ascii','ignore')+'+download&btnI=745'
            webbrowser.open(url, new=0, autoraise=True)
            wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

        elif "weather" in action.lower() and "of" in action.lower():
            city = action[action.index('of')+3:].lower().strip()
            data = retrieve_city_weather_info(city)
            if data is not None:
                systemTalks("The weather of"+city+ "is " + data['description']+"The temperature is" +data['temp']+". The max temperature can be "+data['temp_max']+" and the min temperaute can be"+data['temp_min'] )

            else:
                systemTalks("I could not find this city. Do you want to tell me the city again?")
                wait_anwser = {"active": True, "waiting_command": False, "waiting_anwser":True, "action":"weather", "program": None}

        elif "time now" in action.lower():
            time_now = datetime.now().strftime("%a, %d %b %Y %H:%M")
            print time_now
            systemTalks(time_now)

    elif wait_anwser['active'] == True and wait_anwser["waiting_anwser"] == True:
        if 'yes' in action or 'yep' in action :
            if wait_anwser['action'] == 'download':
                url = 'http://www.google.com/search?hl=en&q='+unicodedata.normalize('NFKD', wait_anwser['program'] + "download")\
                    .encode('ascii','ignore')+'+download&btnI=745'
                webbrowser.open(url, new=0, autoraise=True)
                wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

            if wait_anwser['action'] == 'open':
                os.system(wait_anwser['program'])
                wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

            if wait_anwser['action'] == 'command':
                wait_anwser = {"active": True, "waiting_command": True, "waiting_anwser":False, "action":"command", "program": None}

            if wait_anwser['action'] == 'weather':
                city = action[action.index('yes'):].lower().strip()
                data = retrieve_city_weather_info(city)
                if data is not None:
                   systemTalks("The weather of"+city+ "is " + data['description']+"The temperature is" +data['temp']+". The max temperature can be "+data['temp_max']+" and the min temperaute can be"+data['temp_min'] )

                else:
                    systemTalks("Sorry "+user+". I was not able to find it again.")

                wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}
        elif 'no' in action:
            systemTalks("See you later!")
            wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

        elif action is not "":
            systemTalks("Do you new anything else?")
            wait_anwser = {"active": True, "waiting_command": False, "waiting_anwser":True, "action":"command", "program": None}
        else:
            pass


def listenCommands(source):
    global wait_anwser
    try:
        audio = r.listen(source)
        command = (r.recognize_google(audio, language="en-US"))
        print(command)

        if nickname in command.lower():
            wait_anwser = {"active": True, "waiting_command": True, "waiting_anwser":False, "action":"command", "program": None}
            doAction(command.lower())

        elif wait_anwser["waiting_command"] == True and wait_anwser['active'] == True:
            doAction(command.lower())

        elif wait_anwser['active'] == True and wait_anwser["waiting_anwser"]== True:
            doAction(command.lower())

        else:
            pass


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



def retrieve_city_weather_info(city):
    city = city.replace(' ', '%20')
    weather_doc = {}


    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' +city +'&units=metric&APPID=14f212cb0456519d72374ff4c1f2ad31'
        data = requests.get(url)
        for item in data.json():
            if item == 'weather':
                for element in data.json()['weather']:
                    weather_doc['description'] = element['description']
                    break

            if item == 'main':
                weather_doc['temp'] = str(data.json()['main']['temp']) + " Celsius Degrees"
                weather_doc['temp_max'] = str(data.json()['main']['temp_max']) + " Celsius Degrees"
                weather_doc['temp_min'] = str(data.json()['main']['temp_min']) + " Celsius Degrees"

        return weather_doc
    except:
        return None

def systemTalks(phrase):
    voice = "say -v Alex"
    return os.system( voice + " " + phrase)
    print phrase

def internet_on():

    try:

        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:

        return False


def start():

    while 1:
        if internet_on():

            db.startDB()
            global nickname
            nickname = db.returnDocUser()["callname"]
            systemTalks("Hi, we are ready to start.")
            global r
            r = sr.Recognizer()
            with sr.Microphone() as source:
                while 1:
                    listenCommands(source)
                    print wait_anwser
        else:
            systemTalks('Hey! You are not connect. Try to connect first!')
            time.sleep(60)


start()