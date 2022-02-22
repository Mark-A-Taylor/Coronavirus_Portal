from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Agglomerative Hierarchical Clustering'),
    ),
    html.Br(),
    html.Center(
        html.Div([dcc.Markdown('''
                **TODO:  Chase to fill out this information/functionality**  
                e.g. maybe redirect to a URL with port # serviced by an Rshiny app.
            ''')],
            style={'border': '2px black solid','width':'50%'}
        ),
    ),
    html.Br(),
    html.Div(id='clustering-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])

@app.callback(
    Output('clustering-display-value', 'children'),
    Input('clustering-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)

