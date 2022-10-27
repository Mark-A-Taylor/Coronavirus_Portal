from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
    ),
    html.Br(),
    html.Center(
        #        html.Div([dcc.Markdown('''
        #                **TODO: Insert PDF version of the paper here***  
        #            ''')],
        #            style={'border': '2px black solid','width':'50%'}
        #        ),
        html.Div(
            html.Iframe(id="embedded-pdf",
                        src="/assets/paper_26Aug2022.pdf",
                        style={'height':'800px','width':'98%'},
                        )
        ),
    ),
    html.Br(),
    html.Div(id='paper-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])
