__author__ = 'alex'

import zlib
import pickle as pickle
import time
import uuid

import zmq
import signal


class Task:
    def __init__(self, zpyobj,processorname, expiry=30, retyrcount=3, starttime=None):
        self.zpyobj = zpyobj
        if (starttime == None):
            self.starttime = time.time()
        else:
            self.starttime = starttime
        self.maxretry = retyrcount
        self.retrycount = 0
        self.expiry = expiry
        self.uid = uuid.uuid4()
        self.processorname=processorname

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
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        # load perissted jobs if needed

    def startchecker(self):
        signal.signal(signal.SIGALRM, self.taskchecker)
        signal.setitimer(signal.ITIMER_REAL, 2, 2)

    def taskchecker(self, signum, stack):
        # go throuh the list and check if expiredtask are there
        expiredlist = filter(Task.checkExpiry, self.tasklist)
        # can it be retirued
        retrylist = filter(Task.isRetryExceeded, self.tasklist)
        # Remove the tasks which are expired and retried
        toremove = set(expiredlist).difference(set(retrylist))
        for r in toremove:
            self.tasklist.remove(r)

    def connect(self, port=777, connection="tcp://*"):
        print("Going to connect to %s:%s" % (connection, port))
        self.socket.bind("%s:%s" % (connection, port))
        print("Running TaskSender on port ", port)
        self.__port = port
        self.__connection = connection

    def sendmessage(self, pyobj,processorname, port=777, connection="tcp://*"):
        # socket.send_pyobj(mymessage)
        # better way
        #self.socket.connect("%s:%s" % (connection, port))
        z = zlib.compress(pyobj)
        task = Task(z,processorname)
        self.tasklist.append(task)
        p = pickle.dumps(task)
        self.socket.send(p)
        print("Send the message")


if __name__ == '__main__':
    sender = TaskSender()
    sender.connect()
