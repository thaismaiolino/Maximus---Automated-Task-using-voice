import speech_recognition as sr
import webbrowser
import os
import unicodedata
import appDb as db


global startListening
startListening = False
global nickname


def doAction(a):
        if nickname in a:
            action = a.replace(nickname, "").lstrip(' ')
        else:
            action = a

        if "open" in action.lower():
            if "facebook" in action.lower():
                print action
                url = 'https://www.facebook.com/'
                webbrowser.open(url, new=0, autoraise=True)
                startListening = False
            else:
                program = action.replace("open", "").lstrip(' ')
                print(program)
                tmp = db.returnDocApp(program)
                print (tmp)
                os.system(tmp[0]+"/Contents/MacOS/" + tmp[1])
                startListening = False
        elif "search" in action.lower():
            url = 'https://www.google.com.br/#q=' + unicodedata.normalize('NFKD', action.replace("search", "").lstrip(' ').replace(" ", "+")).encode('ascii','ignore')
            webbrowser.open(url, new=0, autoraise=True)
            startListening = False
        elif "install" in action.lower():
            url = 'http://www.google.com/search?hl=en&q='+unicodedata.normalize('NFKD', action.replace("install", "").lstrip(' ').replace(" ", "+")).encode('ascii','ignore')+'+download&btnI=745'
            webbrowser.open(url, new=0, autoraise=True)
            startListening = False

def listenCommands(source,r):


    try:
        audio = r.listen(source)
        command = (r.recognize_google(audio, language="en-US"))
        print(command)
        if nickname in command.lower():
            startListening = True
            print("entrei aqui")
            doAction(command.lower())
        if startListening == True:
            doAction(command.lower())


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def startListener():
    if __name__ == "__main__":
        db.startDB()
        nickname = db.returnDocUser()["callname"]
        print nickname
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while 1:
                listenCommands(source,r)
