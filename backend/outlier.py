import numpy as np 
import pandas as pd 
from sklearn.ensemble import IsolationForest
import utils 
import config as cng 

class StockOutlierAnalyzer:
    def __init__(self, csv_file: str=None, selected_features: list=None):
        if csv_file is None:
            csv_file = cng.DATASET_FILE

        self.selected_features = selected_features

        self.df_raw = pd.read_csv(csv_file)

    def preprocess(self):
        if self.selected_features is None:
            self.selected_features = cng.SELECTED_FEATURES

        # Note: the dataset consists of data from both Oslo bors' website and yahoo financials. 
        # the two sources may have redundant featutres. Oslo bors' feature will be tagget with
        # '_osebx', and '_yahoo' for yahoo features
        self.df = self.df_raw[self.selected_features]
        

    def run(self):
        self.preprocess()

if __name__ == '__main__':
    anal = StockOutlierAnalyzer()
    anal.run()