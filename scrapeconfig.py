'''
Configurations and strings for scraping stuff
'''

'''General'''
BORS_CSV_NAME = 'borsdata.csv'
YAHOO_CSV_NAME = 'yahoodata.csv'
RETURNS_TARGET_FILE = 'OSEBX_Returns.html'
QUOTES_TARGET_FILE = 'OSEBX_Quotes.html'
BORS_RETURNS_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/return/ob/all/all/false"
BORS_QUOTES_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false"
FINALDATASET_FILENAME = 'OSEBX_dataset.csv'

'''get_rawdata.py'''
RETURNS_WAIT_TARGET_CLASS = 'LONG_NAME'
QUOTES_WAIT_TARGET_CLASS = 'MARKET_CAP'
DEFAULT_BROWSER = 'chrome'
DEFAULT_TIMEOUT = 10

'''datawrangle.py'''
SELECTED_FEATURES = [ 
    'ticker',
    'bookValue',
    'enterpriseValue',
    'trailingEps',
    'forwardEps',
    'priceToBook',
    'beta',
    'profitMargins'
]
MERGE_DFS_ON = 'ticker'

'''common.py'''
BLINK_INTERVAL = 1

