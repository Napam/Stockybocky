from typing import Callable
import pandas as pd 
import yfinance_hotfix as yf 
from pprint import pprint
import re 

df_osebx = pd.read_csv('data/borsdata.csv')

# tickers = ['BOUVET.OL','DNB.OL','AKSO.OL','CRAYON.OL', 'PLT.OL', 'BOUVET.OL', 'EQNR.OL']
# tickers = ['BOUVET.OL','DNB.OL','AKSO.OL']

featdict = {}

for ticker in df_osebx.ticker:
    print(ticker)
    ticker_string = ticker.strip()+'.OL'
    ticker_string = re.sub('\s+','-',ticker_string)
    t = yf.Ticker(ticker_string)
    featdict[ticker] = t.info

df_yahoo = pd.DataFrame(featdict).T
df_yahoo.to_csv('data/yahoodata_test2.csv')






