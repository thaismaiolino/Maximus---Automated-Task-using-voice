import rumps
import SettingsInterface as interface

class SystemTrayApp(rumps.App):
    def __init__(self):

        super(SystemTrayApp, self).__init__("ST")
        self.menu = ["User Settings"]

    @rumps.clicked("Listen")
    def listen(self, _):
        self.title = 'Listening...'
        import assistant
        assistant.start()

    @rumps.clicked("User Settings")
    def settings(self, _):
        print ('before')
        interface.start()
        print ('after')

def start():
    SystemTrayApp().run()

start()