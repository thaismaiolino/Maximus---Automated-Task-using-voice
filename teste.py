import assistant
import sysTray
import random
import multiprocessing


def list_append(count, id, out_list):
    for i in range(count):
        out_list.append(random.random())

def start_assistant():
    assistant.start()

def start_sysTray():
    sysTray.start()

if __name__ == "__main__":
    jobs = []
    t1 = multiprocessing.Process(target=start_assistant)
    t2 = multiprocessing.Process(target=start_sysTray)
    jobs.append(t1)
    jobs.append(t2)

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    print "List processing complete."