from src.processor.TaskListener import TaskProcessor
import resource

__author__ = 'alex'

from  multiprocessing import Process

if __name__ == '__main__':
    print("Worker waiting for Tasks")
    '''rsrc = resource.RLIMIT_DATA
    soft, hard = resource.getrlimit(rsrc)
    print ('Soft limit starts as  :', soft)
    resource.setrlimit(rsrc, (1000*1000*1024, hard))  # limit to one kilobyte
    soft, hard = resource.getrlimit(rsrc)
    print('Soft limit changed to :', soft)'''
    k = TaskProcessor()
    k.connectworkertoport(workerPort=777)
