'''
Run this to get html files

This file contains code to obtain html data from oslo bors and yahoo finance
'''
import numpy as np
import pandas as pd
from selenium import webdriver
import threading
from pprint import pprint
import time
from yahoofinancials import YahooFinancials
from utils import join_threads
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapeconfig as cng

class BaseHandler:
    def __init__(self):
        pass

class BorsHandler:
    def __init__(self):
        pass

class YahooHandler:
    def __init__(self):
        pass

def get_osebx_htmlfile(url: str, targetfile: str, wait_target_class: str=None, timeout: int=cng.DEFAULT_TIMEOUT):
    '''Loads html file using selenium and saves it to disk'''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    # If the webpage dynamically loads the table with the stock information. This code will force the webdriver
    # wait until the wanted element is loaded.
    if not wait_target_class is None:
        try:
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, wait_target_class)))
        except:
            print(f'Timeout: Could not load class {wait_target_class} from {url}')
            driver.quit()
            exit()

    with open(targetfile, 'w+') as file:
        file.write(driver.page_source)

    driver.quit()

def threadgrind(ticker: str, featdict: dict):
    print(f'{ticker} ', end='')
    t = YahooFinancials(ticker+'.OL')
    # t.get_key_statistics_data() returns a dict: TICKER.OL :{bla bla...}
    # Extract values from dict to get nice format
    featdict[ticker] = list(t.get_key_statistics_data().values())[0]
    return

def get_yahoofinancials_keystats(tickers, verbose: bool=True) -> pd.DataFrame:
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
    # get_osebx_htmlfile(cng.BORS_QUOTES_URL, cng.QUOTES_TARGET_FILE, cng.QUOTES_WAIT_TARGET_CLASS)
    # get_osebx_htmlfile(cng.BORS_RETURNS_URL, cng.RETURNS_TARGET_FILE, cng.RETURNS_WAIT_TARGET_CLASS)
    get_yahoofinancials_keystats()