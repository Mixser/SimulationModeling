import threading
from numpy import random
from threading import Lock, Semaphore
from time import sleep
num_call = 0
s = Semaphore(0)

lock = threading.Lock()
time = 10

threads = []
queue = []

def worker():
    while time:
        print time
        s.acquire()
        lock.acquire()
        print 'Wait: ', random.uniform(0, 10)
        print 'POP: ', queue.pop()
        sleep(1)
        lock.release()

def call():
    global num_call
    queue.append(num_call)
    num_call += 1
    s.release()



for i in xrange(2):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()


while time:
    a = random.exponential(2.0)
    print 'Wait for call', a
    call()
    sleep(1)
    time = time - 1

