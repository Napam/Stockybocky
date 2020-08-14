import dash
import analyze as anal

app = dash.Dash(__name__, suppress_callback_exceptions=True,  meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}])
server = app.server

analyzer = anal.StockOutlierAnalyzer()

# Common stuff
name_n_ticker = [f'{name} ({ticker})' for name, ticker in zip(analyzer.df_raw.name, analyzer.df_raw.ticker)]

wanted = [
    'sector_osebx', 
    'priceToBook',
    'trailingPE',
    'forwardPE',
    'averageDailyVolume10Day',
    'averageVolume',
    'profit_today', 
    'profit_1wk', 
    'profit_1month', 
    'profit_ytd',
]

taberu3 = analyzer.df_raw.copy()
df_sector_means = taberu3[wanted].groupby(by='sector_osebx', group_keys=False).mean().reset_index()
df_sector_means = df_sector_means.round(4)