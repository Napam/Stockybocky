from bs4 import BeautifulSoup as bs
import threading 
import time 
import numpy as np 
import sys
from io import StringIO
import scrapeconfig as cng
import consoleconfig as ccng
import os

def print_html(html_test):
    '''To print html containers returned by beautifulsoup4'''
    try:
        strhtml = str(html_test.prettify())
    except:
        strhtml = str(html_test)
    print(strhtml)

    return strhtml