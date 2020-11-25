"""

Utility functions for project 5

"""
import time
from random import randint
def my_wait(start,stop):
    """
    waits a number of seconds randomly selected between start and stop
    """
    if start <= 0:
        start = 10
    
    if stop <= 0:
        stop = 30
    
    if stop <= start:
        stop = start + 10
    
    wait_time = randint(start,stop)
    
    time.sleep(wait_time)
    
    return


def my_print(print_string,debug=0,LOG_FILE=None):
    """
    LOG_FILE = Must be a file handle
    """
    
    if (debug):
        if (LOG_FILE == None):
            print(print_string)
        else:
            print(print_string, file=LOG_FILE)
