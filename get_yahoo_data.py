'''
This code is to obtain key statistics given stock tickers using yahoofinancials. 
The result is a pd.DataFrame with key statistics. 
'''
import numpy as np 
import pandas as pd 
import threading
from pprint import pprint
import time
from yahoofinancials import YahooFinancials 
from common import join_threads
import config as cng 

def threadgrind(ticker: str, featdict: dict):
    print(f'{ticker} ', end='')
    t = YahooFinancials(ticker+'.OL')
    # t.get_key_statistics_data() returns a dict: TICKER.OL :{bla bla...}
    # Extract values from dict to get nice format
    featdict[ticker] = list(t.get_key_statistics_data().values())[0]
    return

def get_keystats(tickers, verbose: bool=True) -> pd.DataFrame:
    featdict = dict()

    threads = [threading.Thread(target=threadgrind, args=(ticker, featdict)) for ticker in tickers]
    print('Starting threads\n')
    # [th.start() for th in threads]
    # Accessing Yahoo too much at once causes it to stop for some reason 
    # Waiting a little before each thread starts helps sometimes 
    for i, th in enumerate(threads):
        th.start()
        time.sleep(0.01)

        if not i % 10:
            print()

    print('\nWaiting for threads\n')

    join_threads(threads, verbose=verbose)
    print() 

    [th.join() for th in threads]

    print('Creating dataframe')
    df = pd.DataFrame(featdict).T
    df.index.name = 'ticker'
    df.reset_index(inplace=True)
    print('Returning dataframe')
    return df

if __name__ == '__main__':
    tickers = pd.read_csv(cng.BORS_CSV_NAME).ticker
    df = get_keystats(tickers)
    df.to_csv(cng.YAHOO_CSV_NAME, index=False)

    
