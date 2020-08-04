import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import dash_table
import analyze as anal
import config as cng
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

a = anal.StockOutlierAnalyzer()

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

taberu3 = a.df_raw.copy()
df_sector_means = taberu3[wanted].groupby(by='sector_osebx', group_keys=False).mean().reset_index()
df_sector_means = df_sector_means.round(4)

print(f'Loading backend at {__name__}')

##########################################################################################################################
##########################################################################################################################
app.layout = html.Div([

dcc.Store(id='storage', storage_type='session', data={'markercolor':'score'}),

html.H1('$tockybocky', id='bockytitle'),

html.P('young mula baby', id='motto'),

html.Div([
    html.Div([
        html.Button('Update features', style={'width':'100%', 'height':'30px'}, 
                    id='update-feats-button', n_clicks=0),

        dcc.Checklist(
            options=[{'label':feat, 'value':feat} for feat in cng.FEATURES],
            value=cng.SELECTED_FEATURES, labelStyle={'display': 'flex'},
            style={'overflowY':'scroll', 
                   'height':'425px', 
                   'border':'1px solid rgb(180,180,180)', 
                   'border-radius':'3px'},
            id='feature-selector',
            persistence=True),

        html.Button('Update plots', style={'width':'100%', 'height':'30px'}, 
                    id='update-plots-button', n_clicks=0),
        
        dcc.Dropdown(
            options=[{'label':feat, 'value':feat} for feat in cng.SELECTED_FEATURES+['score']],
            value='score',
            style={'border':'1px solid rgb(180,180,180)', 
                   'border-radius':'3px'},
            id='plot-color-selector',
            placeholder='Marker color',
            persistence=True),
        
        dcc.Dropdown(
            options=[{'label':feat, 'value':feat} for feat in cng.SELECTED_FEATURES+['score']],
            value='score',
            style={'border':'1px solid rgb(180,180,180)', 
                   'border-radius':'3px',},
            id='plot-size-selector',
            placeholder='Marker size',
            persistence=True),
    
    ], id='features', className='pretty_container'),

    html.Div(id='graphs-div'),

], id='feats-and-graphs'),

html.Div([
    html.Div([dcc.Graph(id='histo')], id='histogram-div', className='pretty_container'),

    html.Div([
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in df_sector_means.columns], 
                             data=df_sector_means.to_dict('records'), 
                             style_table={'overflow':'scroll'})
    ], id='sectorinfo-div', className='pretty_container')
], id='histogram-and-table'),

html.Br(),
html.Div(className='pretty_container', id='bigtable-div'),

html.Div(id='dummydiv', style={'display':'None'})

])
##########################################################################################################################
##########################################################################################################################

def get_graphgrid_html(storage):
    figs = a.get_plots(storage['markercolor'])

    graphgrid = [
        html.Div([
            html.Div([dcc.Graph(id='fig-PCA', figure=figs['PCA'])], className='pretty_container'),
            html.Div([dcc.Graph(id='fig-MDS', figure=figs['MDS'])], className='pretty_container'),
        ], className='row'),

        html.Div([
                html.Div([dcc.Graph(id='fig-LLE', figure=figs['LocallyLinearEmbedding'])], className='pretty_container'),
                html.Div([dcc.Graph(id='fig-ISO', figure=figs['Isomap'])], className='pretty_container'),
        ], className='row')
    ]

    return graphgrid


@app.callback(
    output=[
        Output('graphs-div', 'children'),
        Output('histo', 'figure'),
        Output('bigtable-div', 'children'),],
    inputs=[
        Input('update-feats-button', 'n_clicks')],
    state=[
        State('feature-selector', 'value'), 
        State('storage', 'data')])
def update_features(n_clicks: int, features: list, storage: dict):
    a.preprocess(features)
    dfx = a.fit_and_score()

    dfx.insert(0, 'sector', a.df_raw.sector_osebx)
    dfx.insert(0, 'ticker', a.df_raw.ticker)
    dfx.insert(0, 'name', a.df_raw.name)
    dfx = dfx.sort_values('score')[::-1]
    dfx = dfx.round(4)
    a.get_representations()

    graphgrid = get_graphgrid_html(storage)

    histobisto = a.get_score_hist()

    table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dfx.columns], 
        data=dfx.to_dict('records'), style_table={'overflow':'scroll', 'height':'420px'}, 
        page_size=20, 
        id='bigtable',
    )

    return graphgrid, histobisto, table
    
@app.callback(
    output=[Output('storage', 'data')],
    inputs=[Input('update-plots-button', 'n_clicks')],
    state=[State('plot-color-selector', 'value'), 
           State('plot-size-selector', 'value'),
           State('storage', 'data')])
def update_plots(n_clicks: int, color: str, size: str, data: dict):
    if n_clicks is None:
        raise PreventUpdate

    data['markercolor'] = color
    data['markersize'] = size
    print(data)

    return (data,)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)