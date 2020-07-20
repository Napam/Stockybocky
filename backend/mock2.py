import threading
import time
import random
from typing import List
from math import ceil
import utils
import sys
import pandas as pd 
import numpy as np 

def threadboi(x):
    time.sleep(random.randint(1,5))
    sys.stdout.write(f'{x} ')
    sys.stdout.flush()

def run_threads(threads: List[threading.Thread], chunksize: int=10, start_interval: float=0.01, 
                chunk_interval: float=0):

    n_chunks = ceil(len(threads) / chunksize)
    for i in range(n_chunks):
        sys.stdout.write(f'Chunk {i+1}/{n_chunks}: ')
        sys.stdout.flush()

        threadchunk = threads[i*chunksize:(i+1)*chunksize]
        for thread in threadchunk:
            thread.start()
            time.sleep(start_interval)

        utils.join_threads(threadchunk)
        time.sleep(chunk_interval)
        print()

if __name__ == '__main__':
    df = pd.DataFrame({
        'ticker':['A','B','C','D','E','F','G','H'],
        'price':[1,2,3,4,5,6,7,8],
        'lol':[np.nan, np.nan, 3,4,5,6,7,8],
        'val':[np.nan, np.nan, np.nan, np.nan, 5, 6, 7, 8],
        'lig':[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    })

    series = df.notna().sum(axis=0)/8
    print(series[['ticker','price']])

