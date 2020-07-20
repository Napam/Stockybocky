'''
Configurations and strings for scraping stuff
'''
import datetime as dt
import os

__STR_DATE_TODAY = dt.date.today().strftime("%Y-%m-%d")

'''General'''
DATA_DIR = 'data'
DATA_DATE_DIR = os.path.join(DATA_DIR, __STR_DATE_TODAY)
BORS_CSV_FILE = os.path.join(DATA_DATE_DIR, 'borsdata.csv')
YAHOO_CSV_FILE = os.path.join(DATA_DATE_DIR, 'yahoodata.csv')
RETURNS_HTML_FILE = os.path.join(DATA_DATE_DIR, 'OSEBX_Returns.html')
QUOTES_HTML_FILE = os.path.join(DATA_DATE_DIR, 'OSEBX_Quotes.html')
BORS_RETURNS_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/return/ob/all/all/false"
BORS_QUOTES_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false"
DATASET_FILE = os.path.join(DATA_DATE_DIR, 'stoinks.csv')

'''datapipeline.py'''
RETURNS_WAIT_TARGET_CLASS = 'LONG_NAME'
QUOTES_WAIT_TARGET_CLASS = 'MARKET_CAP'
MERGE_DFS_ON = 'ticker'
DEFAULT_TIMEOUT = 10

'''outlier.py'''

# Features used in ML algorithms
SELECTED_FEATURES = [
    'fullTimeEmployees',
    'twoHundredDayAverage',
    'trailingAnnualDividendYield',
    'payoutRatio',
    'averageDailyVolume10Day',
    'regularMarketPreviousClose',
    'fiftyDayAverage',
    'trailingAnnualDividendRate',
    'averageVolume10days',
    'dividendRate',
    'exDividendDate',
    'beta',
    'regularMarketDayLow',
    'priceHint',
    'currency',
    'trailingPE',
    'regularMarketVolume',
    'averageVolume',
    'priceToSalesTrailing12Months',
    'askSize',
    'volume',
    'fiftyTwoWeekHigh',
    'forwardPE',
    'fiftyTwoWeekLow',
    'dividendYield',
    'bidSize',
    'dayHigh',
    'enterpriseToRevenue',
    'profitMargins',
    '52WeekChange',
    'forwardEps',
    'sharesOutstanding',
    'bookValue',
    'lastFiscalYearEnd',
    'heldPercentInstitutions',
    'netIncomeToCommon',
    'trailingEps',
    'priceToBook',
    'heldPercentInsiders',
    'nextFiscalYearEnd',
    'mostRecentQuarter',
    'floatShares',
    'enterpriseValue',
]

'''utils.py'''
BLINK_INTERVAL = 1

