import numpy as np 
import pandas as pd 
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import utils 
import config as cng 
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json

class StockOutlierAnalyzer:
    def __init__(self, csv_file: str=None, selected_features: list=None):
        if csv_file is None:
            csv_file = cng.DATASET_FILE

        self.selected_features = selected_features

        self.df_raw: pd.DataFrame = pd.read_csv(csv_file)
        self.df: pd.DataFrame = self.df_raw.copy()
        
        self.fitted = False

    def preprocess(self) -> None:
        if self.selected_features is None:
            self.selected_features = cng.SELECTED_FEATURES

        # Note: the dataset consists of data from both Oslo bors' website and yahoo financials. 
        # the two sources may have redundant featutres. Oslo bors' feature will be tagged with
        # '_osebx', and '_yahoo' for yahoo features
        # It is expected that 'sector_osebx' is a feature
        self.df = self.df[self.selected_features]
        
        # Encode string labels to numerical
        self.sectorencoder = LabelEncoder()
        self.df['sector_osebx'] = self.sectorencoder.fit_transform(self.df['sector_osebx'])
        self.dfx = self.df.fillna(0)

    def fit_and_score(self) -> pd.DataFrame:
        # assert self.X is not None, 'Design matrix unavailable, have you called preprocess()?'
        self.detector = IsolationForest() 
        
        if not self.fitted:
            self.detector.fit(self.dfx)
    
        self.scores = self.detector.score_samples(self.dfx)

        dfx_ = self.dfx.copy()
        dfx_.insert(0, 'score', self.scores)
        return dfx_

    def get_representations(self):
        pca = PCA(n_components=2)
        X = pca.fit_transform(self.dfx)
        
        fig = px.scatter(pd.DataFrame(X), x=0, y=1, title='LOL!')

    def run(self):
        self.preprocess()
        self.fit_and_score()
        self.get_representations()

if __name__ == '__main__':
    anal = StockOutlierAnalyzer()
    anal.run()