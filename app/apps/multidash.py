
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import dash_table
import config as cng
from dash.exceptions import PreventUpdate
import common as cmn

cache = {'features':None}

print(f'Loading backend at {__name__}')

##########################################################################################################################
##########################################################################################################################
layout = html.Div([

dcc.Store(id='storage', storage_type='session', data={
    'markercolor':'score',
    'markersize':'marketcap',
    'at_start':False}),

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
            persistence=False),

        html.Button('Update plots', style={'width':'100%', 'height':'30px'}, 
                    id='update-plots-button', n_clicks=0),
        
        html.Div([
            dcc.Dropdown(
                options=[{'label':feat, 'value':feat} for feat in cng.FEATURES+['score']],
                value='score',
                style={'border':'1px solid rgb(180,180,180)', 
                       'border-radius':'3px'},
                id='plot-color-selector',
                placeholder='Marker color',
                persistence=False),
        ], style={'margin-bottom':'10px'}),
        
        html.Div([
            dcc.Dropdown(
                options=[{'label':feat, 'value':feat} for feat in cng.FEATURES+['score']],
                value='marketcap',
                style={'border':'1px solid rgb(180,180,180)', 
                       'border-radius':'3px',},
                id='plot-size-selector',
                placeholder='Marker size',
                persistence=False),
        ]),
    
    ], id='features', className='pretty_container'),

    html.Div(id='graphs-div'),

], id='feats-and-graphs'),

html.Div([
    html.Div([dcc.Graph(id='histo')], id='histogram-div', className='pretty_container'),

    html.Div([
        dash_table.DataTable(columns=[{"name": i, "id": i} for i in cmn.df_sector_means.columns], 
                             data=cmn.df_sector_means.to_dict('records'), 
                             style_table={'overflow':'scroll'})
    ], id='sectorinfo-div', className='pretty_container')
], id='histogram-and-table'),

html.Br(),
html.Div(className='pretty_container', id='bigtable-div'),

html.Div(id='dummydiv', style={'display':'None'})

])
##########################################################################################################################
##########################################################################################################################

@cmn.app.callback(
    output=[
        Output('graphs-div', 'children'),
        Output('histo', 'figure'),
        Output('bigtable-div', 'children'),],
    inputs=[
        Input('update-feats-button', 'n_clicks'),
        Input('update-plots-button', 'n_clicks')],
    state=[
        State('feature-selector', 'value'), 
        State('plot-color-selector', 'value'), 
        State('plot-size-selector', 'value'), 
        State('storage', 'data')])
def update_features(n_clicks_feats: int, n_clicks_plots: int, features: list, color: str, size: str, 
                    storage: dict):
    ctx = dash.callback_context
    prop_id = get_prop_id()

    if (prop_id == 'update-feats-button') or (prop_id is None):
        cmn.analyzer.preprocess(features)
        dfx = cmn.analyzer.fit_and_score()

        dfx.insert(0, 'sector', cmn.analyzer.df_raw.sector_osebx)
        dfx.insert(0, 'name', cmn.name_n_ticker)
        dfx = dfx.sort_values('score')[::-1]
        dfx = dfx.round(4)
        cmn.analyzer.get_representations()

        cache['scorehist'] = cmn.analyzer.get_score_hist()

        cache['bigtable'] = dash_table.DataTable(
            columns=[{'name': i, 'id': i} for i in dfx.columns], 
            data=dfx.to_dict('records'), style_table={'overflow':'scroll', 'height':'700px'}, 
            page_size=20, 
            id='bigtable',
            filter_action='native',
            sort_action='native',
            sort_mode='single',
        )

    elif prop_id == 'update-plots-button':
        storage['markercolor'] = color
        storage['markersize'] = size
    else:
        raise ValueError('Weird stuff hcmn.appening lol')

    graphgrid = get_graphgrid_html(storage['markercolor'], storage['markersize'])

    return graphgrid, cache['scorehist'], cache['bigtable']

def get_prop_id():
    ctx = dash.callback_context
    prop_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if prop_id == '':
        return None

    return prop_id

def get_graphgrid_html(color, size):
    figs = cmn.analyzer.get_plots(color, size)

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

if __name__ == '__main__':
    cmn.app.run_server(host='0.0.0.0', port=80, debug=True)