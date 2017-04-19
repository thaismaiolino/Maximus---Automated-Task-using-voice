import rumps
import SettingsInterface as interface

class SystemTrayApp(rumps.App):
    def __init__(self):

        super(SystemTrayApp, self).__init__("ST")
        self.menu = ["User Settings"]

    @rumps.clicked("User Settings")
    def settings(self, _):
        interface.start()

def start():
    print 'aqui'
    SystemTrayApp().run()
start()