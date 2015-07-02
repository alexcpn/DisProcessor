__author__ = 'alex'

from src.processor.TaskWorker import TaskProcessLTE, TaskProcess3G
from unittest import TestCase
from  src.processor.TaskListener import TaskProcessor
from  src.processor.TaskDistributor import Task
import threading
import zmq
from multiprocessing import Process
import zlib, pickle as pickle
import time


class TestTaskProcessor(TestCase):
    def test_processTask(self):
        testme = TaskProcessor()
        message = TaskProcessLTE("some data")
        testme.processTask(self.doMyProcess, message)
        testme.processTask(print, message)

    def test_connectWorkerToPort(self):
        testme = TaskProcessor();
        server = threading.Thread(target=self.serverpush)
        client = threading.Thread(target=testme.connectworkertoport, args=(777, "ipc://test"))
        client2 = threading.Thread(target=testme.connectworkertoport, args=(777, "ipc://test"))
        print("started thread")
        client.daemon = True
        server.daemon = True
        server.start()
        client.start()
        # client2.start()
        # client2.join(timeout=1)
        client.join(timeout=1)
        server.join(timeout=1)
        print("exited thread")

    def doMyProcess(self, data):
        print("Hey do this process my way")
        print("%s" % data.getprocessor())

    def serverpush(self, port=777):
        context = zmq.Context.instance()
        socket = context.socket(zmq.PUSH)
        socket.bind("ipc://test:%s" % port)
        print("Running server on port ", port)
        mymessage = TaskProcessLTE("Some data")
        #socket.send_pyobj(mymessage)
        #better way
        p=pickle.dumps(mymessage)
        z=zlib.compress(p)
        socket.send(z)
        mymessage = TaskProcess3G("Some data")
        #socket.send_pyobj(mymessage)
        #better way
        p=pickle.dumps(mymessage)
        z=zlib.compress(p)
        socket.send(z)

    def testTaskExpiry(self):
        testme= Task({'rere':1},.5)
        time.sleep(.4)
        self.assertFalse(testme.checkExpiry())
        time.sleep(.2)
        self.assertTrue(testme.checkExpiry())


if __name__ == '__main__':
    print("Going to send a message")
    k = Process(target=TestTaskProcessor.serverpush, args=(777,))
    k.start()
