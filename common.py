from bs4 import BeautifulSoup as bs
import threading 
import time 
import numpy as np 
import sys
from io import StringIO
import scrapeconfig as cng
import consoleconfig as ccng
import os

def print_html(html_test):
    '''To print html containers returned by beautifulsoup4'''
    try:
        strhtml = str(html_test.prettify())
    except:
        strhtml = str(html_test)
    print(strhtml)

    return strhtml

def join_threads(threads: list, verbose: bool = False, blink_interval: int = cng.BLINK_INTERVAL):
    '''
    Join ongoing threads from threading module, has a verbose functionality showing
    the number of active threads.
    '''
    if verbose:
        space = ' '
        backspace = '\b'
        basemsg = "Active threads: "
        basemsglen = len(basemsg)

        sys.stdout.write(basemsg)
        while threading.activeCount() > 1:
            countstring = str(threading.activeCount()-1)
            countlen = len(countstring)
            sys.stdout.write(countstring)
            sys.stdout.flush()

            time.sleep(blink_interval)
            
            # Clears current number of threads from terminal and "resets" cursor 
            sys.stdout.write(backspace*countlen + space*countlen + backspace*countlen)
            sys.stdout.flush()
            
            time.sleep(blink_interval)

        sys.stdout.write(f'\r{space*basemsglen}\r')
        sys.stdout.write('All threads done!')

    [worker.join() for worker in threads]
    return

def case_decorator(func):
    '''Decorator to enforce commmon behavior for cases'''
    def wrapboi(*args, **kwargs):
        clear_screen()
        retobj = func(*args, **kwargs)
        time.sleep(ccng.CASE_EXIT_WAIT_TIME) 
        return retobj

    # "Inherit docstring"
    wrapboi.__doc__ = func.__doc__
    return wrapboi

if __name__ == '__main__':
    def test_join_threads():
        '''Test join_threads using dummy threads'''

        def dummywaiter(maxwait: int=10):
            '''Dummy thread, sleeps for random time between 1 and maxwait (seconds)'''
            time.sleep(np.random.randint(1, maxwait))
            return

        workers = [threading.Thread(target=dummywaiter) for i in range(500)]
        [worker.start() for worker in workers]
        join_threads(workers, verbose=True)

    test_join_threads()