import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
import dash_table
import analyze as anal

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

a = anal.StockOutlierAnalyzer()
a.preprocess()
taberu = a.fit_and_score()
taberu2 = taberu.copy()
taberu2.insert(0, 'ticker', a.df_raw.ticker)
taberu2 = taberu2.sort_values('score')[::-1]
# taberu2 = taberu2.head(50)
fig = a.get_representations()
hist = a.get_score_hist()

app.layout = html.Div([
    html.H1('Stockybocky', id='bockytitle'),

    html.P('young mula baby', id='motto'),

    dcc.Tabs([
        dcc.Tab(label='Representations', value='tab-1'),
        dcc.Tab(label='Stock check', value='tab-2')], 
        id="tabs", value='tab-1'),

    html.Div(id='tabs-content')
])

_repdiv = html.Div([

html.Div([
    html.Div([
        html.Button('Update', style={'width':'100%', 'height':'40px'}, id='update-button'),

        dcc.Checklist(options=[{'label':feat, 'value':feat} for feat in a.selected_features],
        value=a.selected_features, labelStyle={'display': 'flex'},
        style={'overflowY':'scroll', 'height':'920px'})], 

    id='features', className='pretty_container'),

    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='graphy1', figure=fig)], className='pretty_container'),
            html.Div([dcc.Graph(id='graphy2', figure=fig)], className='pretty_container'),
        ], className='row'),

        html.Div([
            html.Div([dcc.Graph(id='graphy3', figure=fig)], className='pretty_container'),
            html.Div([dcc.Graph(id='graphy4', figure=fig)], className='pretty_container'),
        ], className='row'),
    ], id='graphs')
], id='feats-and-graphs'),

html.Div([
    dash_table.DataTable(columns=[{"name": i, "id": i} for i in taberu2.columns], 
    data=taberu2.to_dict('records'), style_table={'overflow':'scroll', 'height':'400px'}, page_size=20)
], className='pretty_container'),

html.Br(),

html.Div([dcc.Graph(id='histo', figure=hist)], className='pretty_container')

], id='front-dash')

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_contect(tab):
    if tab == 'tab-1':
        return _repdiv
    if tab == 'tab-2':
        return html.Div([html.H1('LOL!')])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)