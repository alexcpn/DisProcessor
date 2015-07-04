__author__ = 'alex'

from unittest import TestCase
import time

from processor.taskdistributor import Task, TaskSender


class TestTaskDistributor(TestCase):
    def testTaskCheckerAllExpired(self):
        testme = TaskSender()

        for i in range(1, 10):
            t = Task(expiry=.01, compressedpyobj={"test": i})
            testme.tasklist.append(t)
        time.sleep(.9)
        self.assertTrue(len(testme.tasklist) == 9)
        testme.taskchecker()
        self.assertTrue(len(testme.tasklist) == 0)

    def testTaskCheckerSomeExpired(self):

        testme = TaskSender()
        for i in range(1, 10):
            t = Task(expiry=.01, compressedpyobj={"test": i})
            testme.tasklist.append(t)
        for i in range(1, 10):
            t = Task(expiry=.05, compressedpyobj={"testX": i})
            testme.tasklist.append(t)
        time.sleep(.03)
        self.assertTrue(len(testme.tasklist) == 18)
        testme.taskchecker()
        self.assertTrue(len(testme.tasklist) == 9)
        t = testme.tasklist[0]
        self.assertTrue(t.compressedpyobj["testX"] == 1)
