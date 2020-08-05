import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import multidash, singledash

app.layout = html.Div([

dcc.Location(id='url', refresh=False),

html.Div([
    dcc.Markdown('**Stockybocky**', id='app-title'),
    html.Span(dcc.Markdown("&nbsp young mula baby"), id='motto'),
], id='banner1', className='banner'),

html.Div([
    dcc.Link(dcc.Markdown('**Catdog**'), href='/app1'),
    dcc.Link(dcc.Markdown('**Catdog**'), href='/app1'),
], id='tabs'),

html.Div(id='page-content')


])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/app1':
        return multidash.layout
    elif pathname == '/app2':
        return singledash.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)