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

def start_assistant():
    assistant.start()

def start_sysTray():
    sysTray.start()

if __name__ == "__main__":
    try:
        # Create new threads
        thread1 = myThread('start_assistant')
        thread2 = myThread('sysTray')

        # Start new Threads
        thread1.start()
        thread2.start()
    except Exception as e:

        print e