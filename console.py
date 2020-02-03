import sys 
import os
import strings
import time 
import consoleconfig as cng 

def clear_screen():
    '''Obvious'''
    os.system('cls')

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

def case_decorator(func):
    '''Decorator to enforce commmon behavior for cases'''
    def wrapboi(*args, **kwargs):
        clear_screen()
        retobj = func(*args, **kwargs)
        time.sleep(cng.CASE_EXIT_WAIT_TIME) 
        return retobj
    return wrapboi

@case_decorator
def case1():
    print('Omae wa shinderu')
    time.sleep(1)

@case_decorator
def case2():
    pass

@case_decorator
def case3():
    pass

@case_decorator
def case4():
    pass

@case_decorator
def case5():
    pass

@case_decorator
def exit_program():
    print(strings.EXIT_MSG)
    time.sleep(cng.MSG_WAIT_TIME)
    clear_screen()
    exit()

def main_interface():
    print(strings.START_MSG)

    func_map = {
        '1':(strings.UPDATE_ALL_TITLE, case1),
        '2':(strings.GET_OSLOBORS_TITLE, case2),
        '3':(strings.SCRAPE_OSLOBORS_TITLE, case3),
        '4':(strings.SCRAPE_YAHOO_TITLE, case4),
        '5':(strings.BACKUP_CURRENT_DATA_TITLE, case5),
        '6':(strings.EXIT_TITLE, exit_program)
    }
    
    run = 1
    try:
        while run:
            clear_screen()
            start_menu(func_map)

            # Get key to func map
            # command = input()        
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
    