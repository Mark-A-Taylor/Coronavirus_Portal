from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app


layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Agglomerative Hierarchical Clustering: Cell-cycle Metasignature'),
    ),
    html.Div([
        dcc.Markdown('''
        TODO: User guidance stuff like Vertical axis is ... Horizontal axis is ...
        Hover over the graph to see ... Left-mouse and drag to
        zoom in ... verify html file in 'pages/clustering3.py', etc. ''')
    ]),
    html.Br(),
    html.Center(
        html.Iframe(srcDoc="[placeholder - see pages/clustering3.py to change this]",
                    #TODO: src=app.get_asset_url("74bs_3bv4_4-5TP_hm.html"),
                    style={'height': '1000px', 'width':'98%'},
                   ),
    ),
    html.Br(),
    html.Div(id='clustering3-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])


