__author__ = 'alex'
import math

import numpy


class TaskProcessLTE:
    def getprocessor(self):
        return 'src.processor.TaskWorker.TaskProcessLTE'

    def process(self, *data):
        if data == None:
            raise AssertionError("Empty Data")
        print(list(prime()))
        print("Processed Data LTE %s", data)


class GenericTask:  # TODO: Simulate abstract task here

    def process(self, *args):
        if args == None:
            raise AssertionError("Empty Data")
        print("Processed Data Generic")
        self.processT(args)


class TaskProcess3G(GenericTask):
    def getprocessor(self):
        return 'src.processor.TaskWorker.TaskProcess3G'

    def process(self, *args):
        if args == None:
            raise AssertionError("Empty Data")
        print(args)
        #print("Processed Data 3G  %s " % args.next())


# something that takes time and uses some import like numpy
def prime(upto=100):
    return filter(lambda num: (num % numpy.arange(2, 1 + int(math.sqrt(num)))).all(), range(2, upto + 1))
