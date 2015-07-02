__author__ = 'alex'

import time
import zmq
from pydoc import locate
import zlib, pickle as pickle


class TaskProcessor(object):
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
            #message = self.socketpull.recv_pyobj() better way below
            z=self.socketpull.recv()
            p=zlib.decompress(z)
            message=pickle.loads(p)
            print("Got a message")
            workername = message.getprocessor()
            print("Worker to load is %s" % workername)
            workerclass = locate(workername)
            self.processTask(workerclass.process, message)

    '''
     Takes in a a function object and the function arguments and executes them
    '''

    def processTask(self, processor, *args):
        print("Going to process Task")
        k = processor(*args)
        # Load the python file wiht this name

    def my_import(name):
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod


