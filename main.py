import speech_recognition as sr
import webbrowser
import unicodedata
import appDb as db
import os
import requests

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
        if "open" in action.lower():
            if "facebook" in action.lower():
                url = 'https://www.facebook.com/'
                webbrowser.open(url, new=0, autoraise=True)
                systemTalks("Done. Need something else?")
                wait_anwser = {"active": True, "waiting_command": False, "waiting_anwser":True, "action":None, "program": None}

            else:
                program = action.replace("open", "").lstrip(' ')
                print program
                tmp = db.returnDocApp(program)
                if tmp == "Program not found":
                   systemTalks("You do not have "+program+". Would you like to download it?")
                   wait_anwser = {"active": True,"waiting_command": False, "waiting_anwser":True ,"action":"download", "program": program}

                else:
                    ##### ISN'T BRINGRING THE APP TO THE FRONT. JUST OPEN IN THE BACK. CHANGE IT TO ONE IN FRONT
                    os.system(tmp[0]+"/Contents/MacOS/" + tmp[1])
                    wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

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
                systemTalks("The weather of"+city+ "is " + data['description']+" .") # The temperature is" +data['main']['temp'] )

            else:
                systemTalks("I could not find this city. Do you want to tell me the city again?")
                wait_anwser = {"active": True, "waiting_command": False, "waiting_anwser":True, "action":"weather", "program": None}

    elif wait_anwser['active'] == True and wait_anwser["waiting_anwser"] == True:
        if 'yes' in action or 'yep' in action :
            if wait_anwser['action'] == 'download':
                url = 'http://www.google.com/search?hl=en&q='+unicodedata.normalize('NFKD', wait_anwser['program'] + "download")\
                    .encode('ascii','ignore')+'+download&btnI=745'
                webbrowser.open(url, new=0, autoraise=True)
                wait_anwser = {"active": False, "waiting_command": False, "waiting_anwser":False, "action":None, "program": None}

            if wait_anwser['action'] == 'command':
                wait_anwser = {"active": True, "waiting_command": True, "waiting_anwser":False, "action":"command", "program": None}

            if wait_anwser['action'] == 'weather':
                city = action[action.index('yes'):].lower().strip()
                data = retrieve_city_weather_info(city)
                if data is not None:
                    systemTalks("The weather of"+city+ "is " + data['description']+" .") # The temperature is" +data['main']['temp'] )

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
    final_city = city.replace(' ','%20')
    weather_doc = {}

    print final_city
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q='+final_city+'&APPID=14f212cb0456519d72374ff4c1f2ad31'
        print url

        data = requests.get(url)
        print data
        print data.json()
        for item in data.json():
            if item == 'weather':
                for element in data.json()['weather']:
                    print element['description']
                    weather_doc['description'] = element['description']
                    break

     ########## STILL NEED TO RETRIEVE TEMPERATURE TO ADD TO THE CONVERSATION


            # if item == 'main':
            #     for element in data.json()['main']:
            #
            #         if element == 'temp':
            #             a = (element['temp'])
            #             print a
                    #     weather_doc['temperature'] = str(element['temp'])

                    # if element == 'temp_min':
                    #     print str(element)
                    #     weather_doc['temperature_min'] = str(element['temp_min'])
                    #
                    # if element == 'temp_max':
                    #     print (element['temp_max'])
                    #     weather_doc['temperature_max'] = str(element['temp_max'])

        return weather_doc
    except:
        return None

def systemTalks(phrase):
    voice = "say -v Alex"
    return os.system( voice + " " + phrase)


if __name__ == "__main__":


    db.startDB()
    nickname = db.returnDocUser()["callname"]
    systemTalks("Hi, we are ready to start.")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while 1:
            listenCommands(source)
