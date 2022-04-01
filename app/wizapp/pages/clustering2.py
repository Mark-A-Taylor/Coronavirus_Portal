from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app


layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Agglomerative Hierarchical Clustering: 5 Temporal Meta-Signatures'),
    ),
    html.Div([
        dcc.Markdown('''
        TODO: User guidance stuff like Vertical axis is ... Horizontal axis is ...
        Hover over the graph to see ... Left-mouse and drag to
        zoom in ... verify html file in 'pages/clustering2.py', etc. ''')
    ]),
    html.Br(),
    html.Center(
        html.Iframe(
                    src=app.get_asset_url("3bv2_ave_dpi_genes_int_hm.html"),
                    style={'height': '1067px', 'width':'100%'},
                   ),
    ),
    html.Br(),
    html.Div(id='clustering2-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])


