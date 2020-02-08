'''
Run this to get html files

This file contains code to obtain html data from oslo bors and yahoo finance
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapeconfig as cng 

def get_htmlfile(url: str, targetfile: str, wait_target_class: str=None, timeout: int=cng.DEFAULT_TIMEOUT, 
                 browser: str=cng.DEFAULT_BROWSER):
    '''Loads html file using selenium and saves it to disk'''
    if browser == 'chrome':
        driver = webdriver.Chrome()
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    elif browser == 'opera':
        driver = webdriver.Opera()
    elif browser == 'safari':
        driver = webdriver.Safari()
    else:
        raise ValueError('Invalid browser type, see source code lmao')

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

if __name__ == '__main__':
    get_htmlfile(cng.BORS_QUOTES_URL, cng.QUOTES_TARGET_FILE, cng.QUOTES_WAIT_TARGET_CLASS)
    get_htmlfile(cng.BORS_RETURNS_URL, cng.RETURNS_TARGET_FILE, cng.RETURNS_WAIT_TARGET_CLASS)
