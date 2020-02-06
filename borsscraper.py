'''
This code scrapes data from HTML files from Oslo Bors. 
'''

from bs4 import BeautifulSoup as bs
from pprint import pprint
import numpy as np 
from pandas import DataFrame, to_numeric
from common import print_html
import config as cng
from tqdm import tqdm

def SCRAPE_OSLOBORS_TITLE(quotes: str, returns: str, verbose: bool = False):
    '''
    Scrapes stocks from oslo bors website. HTML of websites of quotes and returns 
    should be located in same folder this file. 

    quotes: https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false
    returns: https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/return/ob/all/all/false
    '''
    with open(quotes) as html_source:
        soup_quotes = bs(html_source, 'lxml')

    with open(returns) as html_source:
        soup_return = bs(html_source, 'lxml')

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

        if verbose:
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
    df.last_ = to_numeric(df.last_)
    df.buy = to_numeric(df.buy, errors='coerce')
    df.sell = to_numeric(df.sell, errors='coerce')
    df.tradecount = to_numeric(df.tradecount)
    return df

if __name__ == '__main__':
    df = SCRAPE_OSLOBORS_TITLE(cng.QUOTES_TARGET_FILE, cng.RETURNS_TARGET_FILE, verbose=False)
    df.to_csv(cng.BORS_CSV_NAME, index=False)
    

    
    




