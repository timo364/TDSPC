# example of sharing a python object using a manager
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing.managers import BaseManager
 
# custom manager to support custom classes
class CustomManager(BaseManager):
    # nothing
    pass
 
# custom function to be executed in a child process
def task(number, shared_set):
    # generate a number
    value = random()
    # block for a moment
    sleep(value)
    # store the result
    shared_set.add((number,value))
 
# protect the entry point
if __name__ == '__main__':
    # register the counter with the custom manager
    CustomManager.register('set', set)
    # create a new manager instance
    with CustomManager() as manager:
        # create a shared set instance
        shared_set = manager.set()
        # start some child processes
        processes = [Process(target=task, args=(i,shared_set)) for i in range(50)]
        # start processes
        for process in processes:
            process.start()
        # wait for processes to finish
        for process in processes:
            process.join()
        # all done
        print('Done')
        # report the results
        print(len(shared_set._getvalue()))
        print(shared_set)