__author__ = 'alex'

from unittest import TestCase
import threading
import time

from processor.taskdistributor import TaskSender
from processor.taskexecutors import TaskProcessLTE,TaskProcess3G
from processor.taskworker import TaskWorker
from  processor.taskdistributor import Task


class TestTaskWorker(TestCase):
    def test_processTask(self):
        testme = TaskProcessLTE()
        worker = TaskWorker()
        message = (self,"43")
        testme3g= TaskProcess3G()
        #worker.processTask(testme.process, message)
        worker.processTask('processor.taskexecutors.TaskProcess3G',*message)


    def test_connectWorkerToPort(self):
        testme = TaskWorker();
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
        client.join(timeout=2)
        server.join(timeout=2)
        print("exited thread")

    def doMyProcess(self, data):
        print("Hey do this process my way")
        print("%s" % data.getprocessor())

    def serverpush(self, port=777, connection='ipc://test'):
        sender = TaskSender()
        sender.connect(port=port, connection=connection)
        myobj = b"testme"
        sender.sendmessage(myobj, 'processor.taskexecutors.TaskProcess3G')
        print("Server Send the message")


    def testTaskExpiry(self):
        testme = Task({'rere': 1},"processarname", .5)
        time.sleep(.4)
        self.assertFalse(testme.checkExpiry())
        time.sleep(.2)
        self.assertTrue(testme.checkExpiry())



