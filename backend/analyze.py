import numpy as np 
import pandas as pd 
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap, LocallyLinearEmbedding, MDS
import utils 
import config as cng 
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
from typing import Callable
import time

def name(obj) -> str:
    '''Get string name of obj, works for functions and instances'''
    return obj.__name__ if isinstance(obj, Callable) else obj.__class__.__name__

def get_visualizations(X: np.ndarray, visualizers: list, verbose: int=0) -> dict:
    '''
    Takes in X and returns a list of all visualizeres from Sklearn-API visualization
    (e.g. UMAP) algorithms. Visualizers should be allocated objects. Returns a dicitonary
    with the names of the visualizers and the values are the result from said visualizer.
    '''
    transforms = dict()
    for i, viz in enumerate(visualizers):
        algoname = name(viz)
        t0 = time.time()
        
        if verbose >= 1: print(f'Running {algoname}', end='')
        temp = viz.fit_transform(X)
        if verbose >= 1: print(f'\r{algoname} transformed in {time.time()-t0:.2f} seconds')
        
        # If same type of function is used multiple times
        if algoname in transforms:
            transforms[algoname+f'{i}'] = temp
        else:
            transforms[algoname] = temp
        
    print()
    return transforms

class StockOutlierAnalyzer:
    def __init__(self, csv_file: str=None, selected_features: list=None):
        if csv_file is None:
            # csv_file = cng.DATASET_FILE
            csv_file = utils.get_latest_dataset()

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
        try:
            self.sectorencoder = LabelEncoder()
            self.df['sector_osebx'] = self.sectorencoder.fit_transform(self.df['sector_osebx'])
        except KeyError as e:
            pass

        self.dfx = self.df.fillna(0)

    def fit_and_score(self) -> pd.DataFrame:
        # assert self.X is not None, 'Design matrix unavailable, have you called preprocess()?'
        self.detector = IsolationForest() 
        
        if not self.fitted:
            self.detector.fit(self.dfx)
    
        self.scores = self.detector.score_samples(self.dfx)

        dfx_ = self.dfx.copy()
        dfx_.insert(0, 'score', -self.scores)
        return dfx_

    def get_representations(self):
        X = self.dfx.values 
        minmaxscaler = MinMaxScaler().fit(X)
        X_minmax = minmaxscaler.transform(X)
        common_viz_kwargs = dict(n_components=3, random_state=cng.SEED)

        vizgroup = [
            MDS(max_iter=200, n_init=4, n_jobs=-1, **common_viz_kwargs), 
            PCA(**common_viz_kwargs), 
            LocallyLinearEmbedding(n_neighbors=69, method='modified', **common_viz_kwargs), 
            Isomap(n_neighbors=30, n_components=3)
        ]

        vizzes = get_visualizations(X_minmax, vizgroup, verbose=1)
        
        pxkwargs = dict(
            x=0, 
            y=1,
            z=2, 
            size=np.log(self.df_raw['marketcap']),
            color=-self.scores,
            # color=self.df_raw['sector_osebx'],
            hover_name=self.df_raw['ticker'],
            width=625,
            height=468,
            color_continuous_scale='viridis',
        )

        figs = {name:px.scatter_3d(pd.DataFrame(X_), title=name, **pxkwargs) for name, X_ in vizzes.items()}

        for fig in figs.values():
            fig.update_layout(showlegend=False)

        return figs

    def get_score_hist(self):

        x = np.quantile(-self.scores, 0.90)

        fig = px.histogram(x=-self.scores, nbins=100, marginal='rug', title=f'90% quantile at {x:.4f}')

        fig.add_shape(
            type="line",
            xref="paper",
            yref="paper",
            x0=x,
            y0=0,
            x1=x,
            y1=1,
            line=dict(
                color='gold',
                width=3,
            ),
        )
        return fig

    def run(self):
        self.preprocess()
        self.fit_and_score()
        self.get_representations()

if __name__ == '__main__':
    anal = StockOutlierAnalyzer()
    anal.run()
    # print(anal.selected_features)