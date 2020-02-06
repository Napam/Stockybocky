from common import case_decorator, clear_screen

@case_decorator
def case1():
    print('Omae wa shinderu')
    time.sleep(1)

@case_decorator
def case2():
    '''
    Obtain Oslo Bors quotes and returns
    '''
    from get_osebx_html_files import get_htmlfile 
    print('Obtaining HTML files from Oslo Bors')
    args = (
        (cng2.BORS_QUOTES_URL, cng2.QUOTES_TARGET_FILE, cng2.QUOTES_WAIT_TARGET_CLASS),
        (cng2.BORS_RETURNS_URL, cng2.RETURNS_TARGET_FILE, cng2.RETURNS_WAIT_TARGET_CLASS)
    )

    threads = [Thread(target=get_htmlfile, args=a) for a in args]
    [th.start() for th in threads]
    cmn.join_threads(threads, verbose=False)
    print('Obtained HTML files')

@case_decorator
def case3():
    '''
    Scrape Oslo bors HTML files
    '''

@case_decorator
def case4():
    '''
    Scrape Yahoo Finance
    '''

@case_decorator
def case5():
    '''
    Backup current data
    '''