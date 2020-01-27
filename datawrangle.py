'''Combines oslo bors and yahoo data'''

import numpy as np 
import pandas as pd 
from pprint import pprint
import config as cng

def merge_bors_and_yahoo_dfs(bors_name: str, yahoo_name: str, result_filename: str):
    '''
    Get filenames for csv files from Oslo Bors and Yahoo Finance and merges them 
    to one large dataset.
    '''
    df_bors = pd.read_csv(bors_name)
    df_stats = pd.read_csv(yahoo_name)

    # Some of the features from Yahoo Finance 
    # are very sparse, so here I am picking the ones 
    # that are not so sparse and that I FEEL makes 
    # makes sense to include.
    df_stats = df_stats[cng.SELECTED_FEATURES]

    df_combined = pd.merge(df_bors, df_stats, on=cng.MERGE_DFS_ON)
    df_combined.set_index(cng.MERGE_DFS_ON, inplace=True)
    df_combined.to_csv(cng.FINALDATASET_FILENAME)

if __name__ == '__main__':
    merge_bors_and_yahoo_dfs(cng.BORS_CSV_NAME, cng.YAHOO_CSV_NAME, cng.FINALDATASET_FILENAME)