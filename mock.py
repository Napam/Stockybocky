def docc():
    '''
    Update all data
    42069
    '''

# print(docc.__doc__.split('\n')[1].strip())
# print(docc.__doc__.strip().split('\n'))
# exit()
import consolecases as cases
import case_decorator
from inspect import getmembers, isfunction, getmodule
import sys

def casefuncchecker(func):
    return True if isfunction(func) and getmodule(func) == cases else False

# lambda f: True if isfunction(func) and getmodule(func) == cases else False

funcs = getmembers(cases, lambda f: True if isfunction(f) and getmodule(f) == cases else False)
print(funcs)


