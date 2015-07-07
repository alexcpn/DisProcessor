__author__ = 'alex'
import math
from random import randint
import time

import numpy


class TaskProcessLTE:
    count=0;


    def getprocessor(self):
        return 'src.processor.TaskWorker.TaskProcessLTE'

    def process(self, *args):
        TaskProcessLTE.count += 1
        if args == None:
            raise AssertionError("Empty Data")
        print(list(prime()))
        print(args)
        print("Processed Data LTE %s " % args[0])
        print("Number of tasks processed LTE =%d" % TaskProcessLTE.count)


class GenericTask:  # TODO: Simulate abstract task here

    def process(self, *args):
        if args == None:
            raise AssertionError("Empty Data")
        print("Processed Data Generic")
        self.processT(args)


class TaskProcess3G(GenericTask):
    count=0

    def getprocessor(self):
        return 'src.processor.TaskWorker.TaskProcess3G'

    def process(self, *args):
        TaskProcess3G.count+=1
        if args == None:
            raise AssertionError("Empty Data")
        print(args)
        time.sleep(randint(1, 9))
        print("Processed Data 3G  %s " % args[0])
        print("Number of 3G tasks processed=%d" % TaskProcess3G.count)


# something that takes time and uses some import like numpy
def prime(upto=100):
    return filter(lambda num: (num % numpy.arange(2, 1 + int(math.sqrt(num)))).all(), range(2, upto + 1))
