def docc():
    '''
    Update all data 
    42069
    '''

print(docc.__doc__.split('\n')[1].strip())

import consolecases as cases
from inspect import getmembers, isfunction
# print(functions_list)
print(isfunction(dir(cases)[-2]))
# functions_list = [o for o in dir(cases) if isfunction(o[1])]