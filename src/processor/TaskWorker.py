__author__ = 'alex'
import math

import numpy


class TaskProcessLTE:
    data = None

    def __init__(self, data):
        self.data = data

    def getprocessor(self):
        return 'src.processor.TaskWorker.TaskProcessLTE'

    def process(self):
        if self.data == None:
            raise AssertionError("Empty Data")
        print(list(prime()))
        print("Processed Data LTE")


class TaskProcess3G:
    data = None

    def __init__(self, data):
        self.data = data

    def getprocessor(self):
        return 'src.processor.TaskWorker.TaskProcess3G'

    def process(self):
        if self.data == None:
            raise AssertionError("Empty Data")
        print("Processed Data 3G")


# something that takes time and uses some import like numpy
def prime(upto=100):
    return filter(lambda num: (num % numpy.arange(2, 1 + int(math.sqrt(num)))).all(), range(2, upto + 1))
