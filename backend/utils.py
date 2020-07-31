from bs4 import BeautifulSoup as bs
import threading 
import time 
import numpy as np 
import pandas as pd 
import sys
import config as cng
from typing import List
import math
import os
import aniso8601

def print_html(html_test):
    '''To print html containers returned by beautifulsoup4'''
    try:
        strhtml = str(html_test.prettify())
    except:
        strhtml = str(html_test)
    print(strhtml)

    return strhtml

def join_threads(threads: list, verbose: int=0, blink_interval: int=cng.BLINK_INTERVAL):
    '''
    Join ongoing threads from threading module, has a verbose functionality showing
    the number of active threads.
    '''
    if verbose >= 1:
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

def run_threads(threads: List[threading.Thread], chunksize: int=10, start_interval: float=0.01, 
                chunk_interval: float=0):
    '''
    Given a list of threads, start threads in chunks. Good for webscraping so website dont get 
    mad. 
    '''
    n_chunks = math.ceil(len(threads) / chunksize)
    for i in range(n_chunks):
        sys.stdout.write(f'Chunk {i+1}/{n_chunks}: ')
        sys.stdout.flush()

        threadchunk = threads[i*chunksize:(i+1)*chunksize]
        for thread in threadchunk:
            thread.start()
            time.sleep(start_interval)

        join_threads(threadchunk)
        time.sleep(chunk_interval)
        print()

def _dump_csv_handler(df: pd.DataFrame, file: str):
    assert type(df) == pd.DataFrame, 'Return value not of type pd.DataFrame'
    df.to_csv(file)

def _dump_txt_handler(s: str, file: str):
    assert type(s) == str, 'Return value not of type str'
    with open(file, 'w+') as f:
        f.write(s)

def dump(file: str, *dumper_args, **dumper_kwargs):
    '''
    Decorator that captures and dumps return value of function.

    Reads filetype from file argument and handles the return value accordingly, supported
    types so far: .csv (pandas), .txt
    '''
    _extension = os.path.splitext(file) 
    
    if _extension == '.txt':
        dump_handler = _dump_csv_handler
    elif _extension == '.csv':
        dump_handler = _dump_txt_handler
    else:
        raise TypeError('Unsupported dump type')

    def decorator(function: Callable):
        def wrapper(*args, **kwargs):
            return_value = function(*args, **kwargs)
            dump_handler(return_value, file, *dumper_args, **dumper_kwargs)
            return return_value
        return wrapper
    return decorator

def get_feature_densities(df: pd.DataFrame):
    return df.notna().sum(axis=0)/len(df)

def get_latest_dataset():
    '''
    Finds directory containing latest dataset
    '''
    dates = os.listdir(cng.DATA_DIR)
    dates = sorted([aniso8601.parse_date(date) for date in dates])
    return os.path.join(cng.DATA_DIR, str(dates[-1]), cng.DATASET_FILE)

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

    # test_join_threads()

    def feat_dens():
        df = pd.read_csv(cng.DATASET_DATE_FILE)
        with pd.option_context('display.max_rows', None):
            print(get_feature_densities(df[cng.SELECTED_FEATURES]).sort_values())
    
    # feat_dens()

    def cat_dog():
        df = pd.read_csv(cng.DATASET_DATE_FILE)
        wanted = [
            'sector_osebx', 
            'priceToBook',
            'trailingPE',
            'forwardPE',
            'averageDailyVolume10Day',
            'averageVolume',
            'profit_today', 
            'profit_1wk', 
            'profit_1month', 
            'profit_ytd',
        ]
        
        df_ = df[wanted]

        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df_.groupby(by='sector_osebx', group_keys=False).mean())
            print(df_.groupby(by='sector_osebx', group_keys=False).std())

    cat_dog()