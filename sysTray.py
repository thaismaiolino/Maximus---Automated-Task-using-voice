import rumps

from Tkinter import *

import appDb as db


global nickname
global user

nickname = db.returnDocUser()["callname"]
user = db.returnDocUser()['user']

class SystemTrayApp(rumps.App):
    def __init__(self):

        super(SystemTrayApp, self).__init__("ST")
        self.menu = ["User Settings", "System Settings"]

    @rumps.clicked("User Settings")
    def settings(self, _):
        pass

    @rumps.clicked("System Settings")
    def settings(self, _):
        rumps.alert("jk! Yes preferences available!")


if __name__ == "__main__":
    SystemTrayApp().run()