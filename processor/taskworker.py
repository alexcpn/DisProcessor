__author__ = 'alex'

import time
import zmq
from pydoc import locate
import zlib, pickle as pickle


class TaskWorker(object):
    context = None
    socketpull = None

    # Init ZeroMQ Context for pull
    def __init__(self):
        self.context = zmq.Context()
        self.socketpull = self.context.socket(zmq.PULL)

    # Poll for Tasks; Listen for a named? socket
    def connectworkertoport(self, workerPort, connection="tcp://localhost"):
        print("Worker Going to Connect  to port %s:%s" % (connection, workerPort))
        self.socketpull.connect("%s:%s" % (connection, workerPort))
        print("Worker Connected to port %s:%s" % (connection, workerPort))
        poller = zmq.Poller()
        poller.register(self.socketpull)

        run = True
        while (run):
            sokcs = dict(poller.poll())
            # message = self.socketpull.recv_pyobj() better way below
            p = self.socketpull.recv()
            mytask = pickle.loads(p)
            taskdata = zlib.decompress(mytask.zpyobj)
            print("Got Task Data- %s" % taskdata)
            workername = mytask.processorname
            # yield
            self.processTask(workername, taskdata)

    '''
     Takes in a a function object and the function arguments and executes them
    '''

    def processTask(self, workername,  *args):
        print("Worker to load is %s" % workername)
        workerclass = locate(workername)
        print("Going to process Task")
        k = workerclass.process(*args)





