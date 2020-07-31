import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import dash_table
import analyze as anal
import config as cng

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

a = anal.StockOutlierAnalyzer()
a.preprocess()
taberu = a.fit_and_score()
taberu2 = taberu.copy()
taberu2.insert(0, 'sector', a.df_raw.sector_osebx)
taberu2.insert(0, 'ticker', a.df_raw.ticker)
taberu2.insert(0, 'name', a.df_raw.name)
taberu2 = taberu2.sort_values('score')[::-1]
taberu2 = taberu2.round(4)
figs = a.get_representations()
hist = a.get_score_hist()

wanted = [
            'sector', 
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

df_sector_means = taberu2[wanted].groupby(by='sector', group_keys=False).mean().reset_index()
df_sector_stds = taberu2[wanted].groupby(by='sector', group_keys=False).std().reset_index()

print('Loaded backend')

##########################################################################################################################
##########################################################################################################################
app.layout = html.Div([



html.H1('Stockybocky', id='bockytitle'),

html.P('young mula baby', id='motto'),

html.Div([
    html.Div([
        html.Button('Update features', style={'width':'100%', 'height':'30px'}, id='update-feats-button', n_clicks=0),

        dcc.Checklist(
            options=[{'label':feat, 'value':feat} for feat in cng.FEATURES],
            value=a.selected_features, labelStyle={'display': 'flex'},
            style={'overflowY':'scroll', 'height':'425px', 'border':'1px solid rgb(180,180,180)', 'border-radius':'3px'},
            id='feature-selector'),

        html.Button('Update plots', style={'width':'100%', 'height':'30px'}, id='update-plots-button', n_clicks=0),
        
        dcc.Checklist(
            options=[{'label':feat, 'value':feat} for feat in cng.SELECTED_FEATURES],
            value=cng.SELECTED_FEATURES, labelStyle={'display': 'flex'},
            style={'overflowY':'scroll', 'height':'425px', 'border':'1px solid rgb(180,180,180)', 'border-radius':'3px'}),
    
    ], id='features', className='pretty_container'),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='fig-PCA', figure=figs['PCA'])], className='pretty_container'),
            html.Div([dcc.Graph(id='fig-MDS', figure=figs['MDS'])], className='pretty_container'),
        ], className='row'),

        html.Div([
            html.Div([dcc.Graph(id='fig-LLE', figure=figs['LocallyLinearEmbedding'])], className='pretty_container'),
            html.Div([dcc.Graph(id='fig-ISO', figure=figs['Isomap'])], className='pretty_container'),
        ], className='row'),
    ], id='graphs')

], id='feats-and-graphs'),

html.Div([
    html.Div([dcc.Graph(id='histo', figure=hist)], id='histogram-div', className='pretty_container'),

    html.Div([
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in df_sector_means.columns], 
        data=df_sector_means.to_dict('records'), style_table={'overflow':'scroll', 'height':'400px'}, 
        page_size=40)], 
    id='sectorinfo-div', className='pretty_container')

], id='histogram-and-table'),

html.Br(),

html.Div([
    dash_table.DataTable(columns=[{"name": i, "id": i} for i in taberu2.columns], 
    data=taberu2.to_dict('records'), style_table={'overflow':'scroll', 'height':'600px'}, page_size=20)
], className='pretty_container'),


])
##########################################################################################################################
##########################################################################################################################

@app.callback(
    output=[Output(component_id='update-plots-button', component_property='children')],
    inputs=[Input(component_id='update-feats-button', component_property='n_clicks')],
    state=[State(component_id='feature-selector', component_property='value')]
)
def update_features(n_clicks, features):
    print(features)
    return ('catdog',)
    

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)