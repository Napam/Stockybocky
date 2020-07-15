from typing import Callable
import pandas as pd 
import yfinance as yf 

tickers = ['BOUVET.OL','DNB.OL','AKSO.OL','CRAYON.OL']

for ticker in tickers:
    print(ticker)
    t = yf.Ticker(ticker)
    t.