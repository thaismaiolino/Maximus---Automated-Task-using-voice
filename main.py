import assistant
import sysTray
from threading import Thread

class myThread (Thread):
    def __init__(self,func):
        Thread.__init__(self)
        self.func= func
    def run(self):
        if self.func == 'assistant':
            start_assistant()
        if self.func == 'sysTray':
            start_sysTray()

def start_assistant(a):
    assistant.start()

def start_sysTray(a):
    sysTray.start()

if __name__ == "__main__":
    try:
        th1 = Thread(target= start_assistant, args=('a') ).start()
        th2 = Thread(target= start_sysTray, args=('a') ).start()

    except Exception as e:

        print e