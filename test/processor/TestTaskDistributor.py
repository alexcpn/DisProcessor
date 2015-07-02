__author__ = 'alex'

from unittest import TestCase
from src.processor.TaskDistributor import  Task, TaskSender

class TestTaskDistributor(TestCase):


    def testTaskChecker(self):
        testme = TaskSender()
        for i in range(1,10):
           t= Task(expiry=.01)
           testme.tasklist.append(t)