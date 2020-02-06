def docc():
    '''
    Update all data 
    42069
    '''

# print(docc.__doc__.split('\n')[1].strip())

# import consolecases as cases
# from inspect import getmembers, isfunction
# print(functions_list)
# print(isfunction(dir(cases)[-2]))
# functions_list = [o for o in dir(cases) if isfunction(o[1])]
from tqdm import tqdm
from time import sleep

gaga = [1,2,3,4,5,6,7,8,9]
gogi = [2,3,4,2,3,4,5,3,3]

for i, j in tqdm(zip(gaga,gogi), total=len(gaga)):
    sleep(0.1)