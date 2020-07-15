'''
Configurations and strings for scraping stuff
'''

'''General'''
BORS_CSV_FILE = 'data/borsdata.csv'
YAHOO_CSV_FILE = 'data/yahoodata.csv'
RETURNS_HTML_FILE = 'data/OSEBX_Returns.html'
QUOTES_HTML_FILE = 'data/OSEBX_Quotes.html'
BORS_RETURNS_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/return/ob/all/all/false"
BORS_QUOTES_URL = "https://www.oslobors.no/ob_eng/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false"
FINALDATASET_FILENAME = 'data/OSEBX_dataset.csv'

'''get_rawdata.py'''
RETURNS_WAIT_TARGET_CLASS = 'LONG_NAME'
QUOTES_WAIT_TARGET_CLASS = 'MARKET_CAP'
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

