import sys 
import os
import strings
import time 
import consoleconfig as cng 
import config as cng2
from threading import Thread
from common import case_decorator, join_threads, clear_screen

def logo_title(title: str):
    '''Prints logo title'''
    print("{:-^40s}".format(title))

def start_menu(func_map: dict):
    '''Prints function map prettily'''
    logo_title(strings.LOGO_TITLE)
    for key, tup in func_map.items():
        print(key + '.', tup[0])  

def enter_prompt():
    '''Prints enter prompt message and than returns input()'''
    print(strings.ENTER_PROMPT, end=' ')
    return input()

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
    join_threads(threads, verbose=False)
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

@case_decorator
def exit_program():
    '''
    Exit program
    '''
    print(strings.EXIT_MSG)
    time.sleep(cng.MSG_WAIT_TIME)
    clear_screen()
    exit()

def construct_func_map(title_func_pairs: list):
    func_map = {}
    for i, pair in enumerate(title_func_pairs, start=1):
        func_map[str(i)] = pair
    return func_map

def main_interface():
    print(strings.START_MSG)

    func_map = construct_func_map([
        (strings.UPDATE_ALL_TITLE, case1),
        (strings.GET_OSLOBORS_TITLE, case2),
        (strings.SCRAPE_OSLOBORS_TITLE, case3),
        (strings.SCRAPE_YAHOO_TITLE, case4),
        (strings.BACKUP_CURRENT_DATA_TITLE, case5),
        (strings.EXIT_TITLE, exit_program)
    ])
    
    run = 1
    try:
        while run:
            clear_screen()
            start_menu(func_map)

            # Get key to func map
            command = enter_prompt()  

            # Pressing enter without specifying input exits program
            if not command:
                exit_program()

            clear_screen()
            if command in func_map:
                func_map[command][1]()
            else:
                print(strings.INVALID_TERMINAL_INPUT_MSG)
                time.sleep(cng.MSG_WAIT_TIME)

    except KeyboardInterrupt:
        # Ensures proper exit when Kbinterrupt
        exit_program()

if __name__ == '__main__':
    main_interface()
    