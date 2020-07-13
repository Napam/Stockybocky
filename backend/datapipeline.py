'''
Run this to get html files

This file contains code to obtain html data from oslo bors and yahoo finance
'''
import threading
import time
from pprint import pprint

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from pandas import DataFrame, to_numeric
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from yahoofinancials import YahooFinancials

import scrapeconfig as cng
from utils import join_threads, print_html

def dump_assert(file: str):
    assert file is not None, 'File parameter must be specified when dump=True'

def get_osebx_htmlfile(url: str, timeout: int=cng.DEFAULT_TIMEOUT, wait_target_class: str=None, 
                       verbose: int=1, dump: bool=True, file: str=None) -> str:
    '''Loads html file using selenium'''

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    if verbose >= 1: print('Initialized chromedriver')

    driver.get(url)

    if verbose >= 1: print('Waiting for target HTML class to appear')

    # If the webpage dynamically loads the table with the stock information. This code will force the webdriver
    # wait until the wanted element is loaded.
    if not wait_target_class is None:
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, wait_target_class))
            )
        except:
            print(f'Timeout: Could not load class {wait_target_class} from {url}')
            driver.quit()
            exit()

    if verbose >= 1: print('Element located')

    page_src = driver.page_source
    driver.quit()

    if dump:
        if verbose >= 1: print(f'Dumping HTML file: {file}')
        dump_assert(file)
        with open(file, 'w+') as file:
            file.write(page_src)

    return page_src

def scrape_osebx_html(quotes: str, returns: str, verbose: int=0, dump: bool=True, 
                      file: str=None) -> pd.DataFrame:
    '''
    Scrapes stocks from oslo bors website. HTML of websites of quotes and returns 
    should be located in same folder this file. 

    quotes: https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false
    returns: https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/return/ob/all/all/false
    '''
    with open(quotes) as html_source:
        soup_quotes = bs(html_source, 'html.parser')

    with open(returns) as html_source:
        soup_return = bs(html_source, 'html.parser')

    # Filter out the stock tables 
    html_quotes = soup_quotes.find('div', class_="ng-scope").find('ui-view').find('ui-view').find('tbody').find_all('tr')
    html_return = soup_return.find('div', class_="ng-scope").find('ui-view').find('ui-view').find('tbody').find_all('tr')
    
    tickers = []
    names = []
    lasts = []
    buys = []
    sells = []
    tradecounts = []
    marketcaps = []
    sectors = []
    infos = []
    profits_today = []
    profits_1wk = []
    profits_1month = []
    profits_ytd = []
    profits_1yr = []

    # Create lists with features. Only preprocessing for strings are done (values are all strings). 
    # Further preprocessing will be done later when the values are in a pandas DataFrame. 
    for quotesrow, returnrow in tqdm(zip(html_quotes, html_return), total=len(html_quotes), disable=verbose):
        # Scrape ticker, name, marketcap, sector and info. 
        tickers.append(quotesrow.a.text)
        names.append(quotesrow.find('td', {'data-header':'Navn'}).text)
        lasts.append(quotesrow.find('td', {'data-header':'Last'}).text.replace(',', ''))
        buys.append(quotesrow.find('td', {'data-header':'Buy'}).text.replace(',', ''))
        sells.append(quotesrow.find('td', {'data-header':'Sell'}).text.replace(',', ''))
        tradecounts.append(quotesrow.find('td', {'data-header':'No. of trades'}).text.replace(',', ''))
        marketcaps.append(quotesrow.find('td', {'data-header':'Market cap (MNOK)'}).text.replace(',', ''))
        # Marketcap unit is in millions, multiply by 10e6 to get normal values
        sectors.append(quotesrow.find('td', class_='icons').get('title'))
        # Info is whether instrument is a Liquidit y provider or not
        infos.append('LP' if 'fa-bolt' in quotesrow.find('td', class_='infoIcon').i.get('class') else np.nan)

        # Scrape return values
        # Values are percentages, and are currently in text form. Divide by 100 to get normal values
        profits_today.append(returnrow.find('td', class_='CHANGE_PCT_SLACK').text.replace('%', ''))
        profits_1wk.append(returnrow.find('td', class_='CHANGE_1WEEK_PCT_SLACK').text.replace('%', ''))
        profits_1month.append(returnrow.find('td', class_='CHANGE_1MONTH_PCT_SLACK').text.replace('%', ''))
        profits_ytd.append(returnrow.find('td', class_='CHANGE_YEAR_PCT_SLACK').text.replace('%', ''))
        profits_1yr.append(returnrow.find('td', class_='CHANGE_1YEAR_PCT_SLACK').text.replace('%', ''))

        if verbose >= 1:
            print(f'Ticker: {tickers[-1]}')
            print(f'Name: {names[-1]}')
            print(f'Last: {lasts[-1]}')
            print(f'Buy: {buys[-1]}')
            print(f'Sell: {sells[-1]}')
            print(f'Cap: {marketcaps[-1]}')
            print(f'Sector: {sectors[-1]}')
            print(f'Info: {infos[-1]}')
            print(f'Profit today: {profits_today[-1]}')
            print(f'Profit 1 week: {profits_1wk[-1]}')
            print(f'Profit 1 month: {profits_1month[-1]}')
            print(f'Profit YTD: {profits_ytd[-1]}')
            print(f'Profit 1 year: {profits_1yr[-1]}')
            print()

    df = DataFrame(dict(
        ticker=tickers,
        name=names,
        sector=sectors,
        last_=lasts, # DataFrame.last is a method, hence the underscore
        buy=buys,
        sell=sells,
        tradecount=tradecounts,
        info=infos,
        marketcap=marketcaps,
        profit_today=profits_today,
        profit_1wk=profits_1wk,
        profit_1month=profits_1month,
        profit_ytd=profits_ytd,
        profit_1yr=profits_1yr
    ))

    # Turn returns to floats then divide by 100 to convert from percentages to "numbers"
    columns_to_num = ['profit_today', 'profit_1wk', 'profit_1month', 'profit_ytd', 'profit_1yr']
    df[columns_to_num] = df[columns_to_num].apply(to_numeric, errors='coerce') / 100

    # Turn other things to numeric as well 
    # coerce turns missing or invalid values to nan
    df.last_ = to_numeric(df.last_, errors='coerce')
    df.buy = to_numeric(df.buy, errors='coerce')
    df.sell = to_numeric(df.sell, errors='coerce')
    df.tradecount = to_numeric(df.tradecount, errors='corce')

    if dump:
        dump_assert(file)
        df.to_csv(file)

    return df

def yahoo_querier_(ticker: str, featdict: dict) -> None:
    '''
    Adds ticker information to dictionary inplace
    '''
    print(f'{ticker} ', end='')
    t = YahooFinancials(ticker+'.OL')
    # t.get_key_statistics_data() returns a dict: TICKER.OL :{bla bla...}
    # Extract values from dict to get nice format
    featdict[ticker] = list(t.get_key_statistics_data().values())[0]
    return

def get_yahoofinancials_keystats(tickers, verbose: int=1, dump: bool=True, file: str=None) -> pd.DataFrame:
    featdict = dict()

    threads = [threading.Thread(target=yahoo_querier_, args=(ticker, featdict)) for ticker in tickers]

    if verbose >= 2: print('Starting threads\n')

    # [th.start() for th in threads]

    # Accessing Yahoo too much at once causes it to stop for some reason
    # Waiting a little before each thread starts helps sometimes
    for i, th in enumerate(threads):
        th.start()
        time.sleep(0.05)

        if verbose >= 1:
            if not i % 10:
                print()

    if verbose >= 2: print('\nWaiting for threads\n')

    join_threads(threads, verbose=verbose)
    if verbose >= 1: print()

    [th.join() for th in threads]

    if verbose >= 2: print('Creating dataframe')
    df = pd.DataFrame(featdict).T
    df.index.name = 'ticker'
    df.reset_index(inplace=True)
    if verbose >= 2: print('Returning dataframe')

    if dump:
        dump_assert(file)
        df.to_csv(file)

    return df

def run_datapipeline():

    # get_osebx_htmlfile(url=cng.BORS_QUOTES_URL,
    #                    wait_target_class=cng.QUOTES_WAIT_TARGET_CLASS,
    #                    dump=True,
    #                    file=cng.QUOTES_HTML_FILE)

    # get_osebx_htmlfile(url=cng.BORS_RETURNS_URL,
    #                    wait_target_class=cng.RETURNS_WAIT_TARGET_CLASS,
    #                    dump=True,
    #                    file=cng.RETURNS_HTML_FILE)

    scrape_osebx_html(quotes=cng.QUOTES_HTML_FILE, 
                      returns=cng.RETURNS_HTML_FILE, 
                      verbose=2, 
                      dump=True, 
                      file=cng.BORS_CSV_FILE)

if __name__ == '__main__':
    run_datapipeline()
    pass
