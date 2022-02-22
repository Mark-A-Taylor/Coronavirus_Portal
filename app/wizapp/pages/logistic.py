from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Elastic Net Logistic Model with Regularization'),
    ),
    html.Br(),
    html.Center(
        html.Div([dcc.Markdown('''
                **TODO:  Frank to fill out this information/functionality**
            ''')],
            style={'border': '2px black solid','width':'50%'}
        ),
    ),
    html.Br(),
    html.Div(id='logistic-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])

