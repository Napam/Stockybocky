'''
Configurations and strings for scraping stuff
'''
import datetime as dt
import os

SEED = 42069

DATE_FORMAT = "%Y-%m-%d"
__STR_DATE_TODAY = dt.date.today().strftime(DATE_FORMAT)

'''General'''
DATA_DIR = 'data'
BORS_CSV_FILE = 'osebxdata.csv'
YAHOO_CSV_FILE = 'yahoodata.csv'
RETURNS_HTML_FILE = 'OSEBX_Returns.html'
QUOTES_HTML_FILE = 'OSEBX_Quotes.html'
BORS_RETURNS_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/return/ob/all/all/false"
BORS_QUOTES_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false"
DATASET_FILE = 'stoinks.csv'

DATA_DATE_DIR = os.path.join(DATA_DIR, __STR_DATE_TODAY)
BORS_CSV_DATE_FILE = os.path.join(DATA_DATE_DIR, BORS_CSV_FILE)
YAHOO_CSV_DATE_FILE = os.path.join(DATA_DATE_DIR, YAHOO_CSV_FILE)
RETURNS_HTML_DATE_FILE = os.path.join(DATA_DATE_DIR, RETURNS_HTML_FILE)
QUOTES_HTML_DATE_FILE = os.path.join(DATA_DATE_DIR, QUOTES_HTML_FILE)
DATASET_DATE_FILE = os.path.join(DATA_DATE_DIR, DATASET_FILE)

'''datapipeline.py'''
RETURNS_WAIT_TARGET_CLASS = 'LONG_NAME'
QUOTES_WAIT_TARGET_CLASS = 'MARKET_CAP'
MERGE_DFS_ON = 'ticker'
DEFAULT_TIMEOUT = 10

'''outlier.py'''

# Features used in ML algorithms
FEATURES_YAHOO = [
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

FEATURES_OSEBX = [
    'sector_osebx',
    'name',
    'last_',
    'buy',
    'sell',
    'tradecount',
    'marketcap',
    'profit_today',
    'profit_1wk',
    'profit_1month',
    'profit_ytd',
    'profit_1yr'
]

FEATURES = sorted(FEATURES_OSEBX + FEATURES_YAHOO)
SELECTED_FEATURES = sorted([
    'profit_today',
    'profit_1wk',
    'profit_1month',
    'profit_ytd',
    'profit_1yr',
    'fullTimeEmployees',
    'averageDailyVolume10Day',
    'fiftyDayAverage',
    'averageVolume10days',
    'exDividendDate',
    'beta',
    'priceHint',
    'trailingPE',
    'regularMarketVolume',
    'averageVolume',
    'priceToSalesTrailing12Months',
    'askSize',
    'volume',
    'forwardPE',
    'bidSize',
    'enterpriseToRevenue',
    'profitMargins',
    'forwardEps',
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
])

'''utils.py'''
BLINK_INTERVAL = 1

