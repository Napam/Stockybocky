import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import common as cmn
from apps import multidash, singledash
from common import server

#####################################################################################################################
#####################################################################################################################
cmn.app.layout = html.Div([

dcc.Location(id='url', refresh=False),

html.Div([
    html.Div([
        html.Div([
            dcc.Markdown('**Stockybocky**', id='app-title'),
            dcc.Markdown('&nbsp young mula baby', id='motto')
        ], className='inner-banner', id='inner-banner-logo'),
    ], id='banner-logo'),

    html.Div([
        html.Div(className='inner-banner', id='links'),
    ], id='banner-links-container'),

], id='banner1', className='banner'),

html.Div(id='page-content')


])
#####################################################################################################################
#####################################################################################################################

@cmn.app.callback(
    output=[
        Output('page-content', 'children'),
        Output('links', 'children'),],
    inputs=[
        Input('url', 'pathname')])
def display_page(pathname):
    links = (
        dcc.Link('Outlier analysis', href='/app1'),
        dcc.Link('Stock analysis', href='/app2'),
    )

    if pathname == '/app1':
        links[0].children = dcc.Markdown('**&#9632 Outlier analysis**')
        _layout = multidash.layout
    elif pathname == '/app2':
        links[1].children = dcc.Markdown('**&#9632 Stock analysis**')
        _layout = singledash.layout
    else:
        _layout = 'Lol!!!'

    return _layout, links

if __name__ == '__main__':
    cmn.app.title = 'Stockybocky'
    cmn.app.run_server(debug=True, host='0.0.0.0', port=80)