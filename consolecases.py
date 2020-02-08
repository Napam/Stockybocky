'''
File containing cases for console interface

Each case should be a function.
The ordering of the cases in the console interface
will be by the function names. So a() will be 
first then b() etc.

Name of cases in console interface will be first line of 
docstring

Feel free to import whatever
'''
from common import join_threads
from threading import Thread
from pandas import to_numeric 
from time import sleep
import scrapeconfig as scng
import numpy as np
from consoleobject import CLI
from consoledecorator import case_decorator
from borsscraper import SCRAPE_OSLOBORS_TITLE
from pandas import read_csv
from get_yahoo_data import get_keystats
from datawrangle import merge_bors_and_yahoo_dfs

def a1_datagathering():
    '''Data wrangling and scraping'''

    def b1_updateall():
        '''
        Update all data
        '''
        b2_obtainbors()
        b3_scrapebors()
        b4_scrapeyahoo()
        b5_merge()

    def b2_obtainbors():
        '''
        Obtain Oslo Bors quotes and returns
        '''
        from get_osebx_html_files import get_htmlfile 
        print('Obtaining HTML files from Oslo Bors')
        args = (
            (scng.BORS_QUOTES_URL, scng.QUOTES_TARGET_FILE, scng.QUOTES_WAIT_TARGET_CLASS),
            (scng.BORS_RETURNS_URL, scng.RETURNS_TARGET_FILE, scng.RETURNS_WAIT_TARGET_CLASS)
        )

        threads = [Thread(target=get_htmlfile, args=a) for a in args]
        [th.start() for th in threads]
        join_threads(threads, verbose=False)
        print('Obtained HTML files')


    def b3_scrapebors():
        '''
        Scrape Oslo bors HTML files
        '''
        print('Scraping HTML files')
        df = SCRAPE_OSLOBORS_TITLE(scng.QUOTES_TARGET_FILE, scng.RETURNS_TARGET_FILE, verbose=False)
        df.to_csv(scng.BORS_CSV_NAME, index=False)


    def b4_scrapeyahoo():
        '''
        Scrape Yahoo Finance
        '''
        print('Obtaining key statistics from Yahoo Financials')
        tickers = read_csv(scng.BORS_CSV_NAME).ticker
        df = get_keystats(tickers)
        df.to_csv(scng.YAHOO_CSV_NAME, index=False)


    def b5_merge():
        '''
        Get csv dataset
        '''
        print('Compiling data into one dataset')
        merge_bors_and_yahoo_dfs(scng.BORS_CSV_NAME, scng.YAHOO_CSV_NAME, scng.FINALDATASET_FILENAME)

    CLI(cases=list(locals().values()), title= ' Data stuff ', decorator=case_decorator).run()

def a6():
    '''
    Data science
    '''
    def b1():
        '''Get top 20 outliers'''
        print('WIP')
    
    def b2():
        '''Describe top 20 outliers'''
        print('WIP')

    CLI([b1, b2], title=' Unsupervised learning ', decorator=case_decorator).run()
