__author__ = 'alex'

import zlib
import pickle as pickle
import time
import uuid

import zmq
import signal


class Task:
    def __init__(self, compressedpyobj, expiry=30, retyrcount=3, starttime=None):
        self.compressedpyobj = compressedpyobj
        if (starttime == None):
            self.starttime = time.time()
        else:
            self.starttime = starttime
        self.maxretry = retyrcount
        self.retrycount = 0
        self.expiry = expiry
        self.uid = uuid.uuid4()

    def checkExpiry(self):
        if (time.time() - self.starttime > self.expiry):
            return True
        return False

    def incrretry(self):
        self.retrycount += 1

    def isRetryExceeded(self):
        if (self.retrycount > self.maxretry):
            return True
        return False


class TaskSender:
    tasklist = []

    def __init__(self):
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.PUSH)
        signal.signal(signal.SIGALRM, self.taskchecker)
        signal.setitimer(signal.ITIMER_REAL, 2, 2)
        # load perissted jobs if needed

    def taskchecker(self):
        # go throuh the list and check if expiredtask are there
        expiredlist = filter(Task.checkExpiry, self.tasklist)
        # can it be retirued
        retrylist = filter(Task.isRetryExceeded,self.tasklist)
        #Remove the tasks which are expired and retried
        toremove= set(expiredlist).difference(set(retrylist))
        for r in toremove:
            self.tasklist.remove(r)

        def connect(self, port=777, connection="tcp://localhost"):
            self.socket.bind("%s:%s" % (connection, port))
            print("Running TaskSender on port ", port)

        def sendmessage(self, pyobj):
            # socket.send_pyobj(mymessage)
            # better way
            p = pickle.dumps(pyobj)
            z = zlib.compress(p)
            task = Task(z)
            self.tasklist.append(task)
            self.socket.send(task)
