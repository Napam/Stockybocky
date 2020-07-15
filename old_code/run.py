import scrapeconfig as cng
import pandas as pd 
from get_osebx_html_files import get_htmlfile 
from get_yahoo_data import get_keystats
from datawrangle import merge_bors_and_yahoo_dfs
from borsscraper import SCRAPE_OSLOBORS_TITLE

if __name__ == '__main__':
    # Obtain HTML pages of Oslo Bors 
    # print('Obtaining HTML files from Oslo Bors')
    get_htmlfile(url=cng.BORS_QUOTES_URL, targetfile=cng.QUOTES_TARGET_FILE, wait_target_class=cng.QUOTES_WAIT_TARGET_CLASS)
    get_htmlfile(url=cng.BORS_RETURNS_URL, targetfile=cng.RETURNS_TARGET_FILE, wait_target_class=cng.RETURNS_WAIT_TARGET_CLASS)

    # Scrape HTML files
    print('Scraping HTML files')
    df = SCRAPE_OSLOBORS_TITLE(cng.QUOTES_TARGET_FILE, cng.RETURNS_TARGET_FILE, verbose=False)
    df.to_csv(cng.BORS_CSV_NAME, index=False)

    # Obtain key statistics from YahooFinancials
    # This part requires that the files from the previous step 
    # are available in order to get the tickers
    # May take some time 
    print('Obtaining key statistics from Yahoo Financials')
    tickers = pd.read_csv(cng.BORS_CSV_NAME).ticker
    df = get_keystats(tickers)
    df.to_csv(cng.YAHOO_CSV_NAME, index=False)

    print('Compiling data')
    # Get a combined dataset consisting of data from Oslo Bors and YahooFinancials
    merge_bors_and_yahoo_dfs(cng.BORS_CSV_NAME, cng.YAHOO_CSV_NAME, cng.FINALDATASET_FILENAME)
    print('Done!')

