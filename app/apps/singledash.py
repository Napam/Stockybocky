
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import dash_table
import config as cng
import common as cmn
cmn.analyzer.preprocess()
##########################################################################################################################
##########################################################################################################################
layout = html.Div([

html.Div([
    dcc.Dropdown(
        options=[{'label':label, 'value':ticker} for label, ticker in 
                 zip(cmn.name_n_ticker, cmn.analyzer.df_raw.ticker)],
        value=cmn.analyzer.df_raw.ticker[0],
        multi=False,
        id='tickerpicker'),
], className='pretty_container'),

html.Div([
    html.Div([

    ], id='pe_hist')
], className='pretty_container')

])
##########################################################################################################################
##########################################################################################################################

if __name__ == '__main__':
    cmn.app.run_server(host='0.0.0.0', port=80, debug=True)