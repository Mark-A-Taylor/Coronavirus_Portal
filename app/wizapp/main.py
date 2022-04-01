import sys
import os
import getopt
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import inspect

# unique to this application
from app import app
from pages import pca, clustering, clustering2, clustering3, timeseries, logistic, methods, datatable, paper

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
       html.H2('Crowdsourcing Temporal Transcriptomic Coronavirus Host Infection Data'),
       dcc.Markdown('''
            Welcome!  Please use the links below to explore the data related to our paper of meta-analysis of
            host responses to SARS-CoV-1 infection.
       '''),
       html.Center(
           html.Div(
               [
                   html.Div(
                       html.H3('Systemic Review of Omic-scale Studies and Experimental Designs in BSCE')
                   ),
                   html.Div([
                        dcc.Markdown('''[View paper](/pages/paper)'''),
                        # FUTURE: html.A('Paper', href='https://link.to.paper',target='_blank')
                   ]),
                   html.Div([
                       html.A('Github repository', href='https://github.com/Mark-A-Taylor/Coronavirus_Portal.git/',target='_blank'),
                    ], style={'margin-bottom':10}
                   ),
               ],
               id='button1',
               style={'border':'2px black solid'}
           ),
       ),
       html.Br(),
    html.Center(
        html.Div([dcc.Markdown('''
                [**Data**](/pages/datatable)  
                74 SARS-CoV-1 lung infected vs mock infected Biosets
                5 Time Points (0.5, 1, 2, 4 and 7 days post-infection)  
                3 Age Groups (young, adult, aged)  
                5 viral variants (low severity to lethal)  
                4 magnitudes of viral dose  
                299 experimental and 239 control mice (3 host strains)  
            ''')],
            style={'border': '2px black solid','width':'50%'}
        ),
    ),
    html.Br(),
    html.Center(
        html.Div([dcc.Markdown('''
                ** [Methods](/pages/methods) **  
            ''')],
                 style={'border': '1px black solid','width':'10%'}
                 ),
    ),
    html.Div(
        html.Img(src=app.get_asset_url('triarrow.png'), style={'height':'50%', 'width':'50%'}, id='triarrow'),
      style={'textAlign':'center'}
    ),
    html.Center(
        html.Div([
            html.Div([
                html.Center([
                    dcc.Markdown('''
                        **Unsupervised Machine Learning**  
                        [Principal Component Analysis](/pages/pca)  
                        [Agglomerative Hierarchical Clustering](/pages/clustering)  
                    ''')], style={'margin-right':10,'margin-left':10},
                    #removed: [Cell-cycle metasignature](/pages/clustering3)
                ),
            ], style={'display':'inline-block','border': '2px black solid','margin-right':10,'verticalAlign':'middle'}),
            html.Div([
                html.Center(
                    dcc.Markdown('''
                        ** 5 Temporal Meta-Signatures **  
                        [Line Plots](/pages/timeseries)  
                        [Agglomerative Hierarchical Clustering](/pages/clustering2)  
                    '''), style={'margin-right':10,'margin-left':10},
                ),
            ], style={'display':'inline-block','border': '2px black solid','margin-right':10,'verticalAlign':'middle'}),
            html.Div([
                html.Center(
                    dcc.Markdown('''
                        **Supervised Machine Learning**  
                       [ Elastic Net Logistic Model  
                        with Regularization ](/pages/logistic)  
                    '''), style={'margin-right':10,'margin-left':10},
                ),
            ], style={'display':'inline-block','border': '2px black solid','verticalAlign':'middle'}),
            ]),
    ),
    html.Center([
        # begin left block
        html.Div([
            html.Img(src=app.get_asset_url('downRightArrow.jpg'), style={'height': '165%', 'width':'165%'}),
        ], style={'display': 'inline-block', 'verticalAlign': 'middle','margin-top':20}), #({,'border':'2px green solid'}),

        # begin center block
        html.Div([
            html.Div(
                html.Img(src=app.get_asset_url('triarrow.png'), style={'height': '40%', 'width': '60%'}),
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.Center(
                            dcc.Markdown('''Similarity Profiling'''), style={'margin-right': 5, 'margin-left': 5},
                        ),
                    ], style={'border': '1px black solid', 'verticalAlign': 'middle'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('downAngleRightArrow.jpg'), style={'height': '75%', 'width': '75%'}),
                    ], style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                ], style ={'display':'inline-block','margin-right':5,'margin-top':5,'verticalAlign':'middle'}
                ),
                html.Div([
                    html.Div([
                        html.Center(
                            dcc.Markdown('''Functional Enrichment '''), style={'margin-right': 5, 'margin-left': 5},
                        ),
                    ], style={'border': '1px black solid', 'verticalAlign': 'middle'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('downArrow.jpg'), style={'height': '75%', 'width': '75%'}),
                    ], style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                ], style ={'display':'inline-block','margin-right':5,'margin-top':4,'verticalAlign':'middle'}
                ),
                html.Div([
                    html.Div([
                        html.Center(
                            dcc.Markdown('''Compound Discovery'''), style={'margin-right': 5, 'margin-left': 5},
                        ),
                    ], style={'border': '1px black solid', 'verticalAlign': 'middle'}),
                    html.Div([
                        html.Img(src=app.get_asset_url('downAngleLeftArrow.jpg'), style={'height': '75%', 'width': '75%'}),
                    ], style={'display': 'inline-block', 'verticalAlign': 'middle'}),
                ], style ={'display':'inline-block','margin-right':5,'verticalAlign':'middle'}
                ),
            ]),
            html.Div([
                html.Center(
                    html.H3('Interpretation, Synthesis and Impact'),
                    style={'margin-right': 5, 'margin-left': 5, 'color':'green'},
                ), ], style={'border': '2px black solid'}),
        ], style={'display': 'inline-block', 'verticalAlign': 'middle','margin-right':15,'margin-left':55}),
        # end center block

        # begin right block
        html.Div([
            html.Img(src=app.get_asset_url('downLeftArrow.jpg'), style={'height': '175%', 'width':'175%'}),
        ], style={'display': 'inline-block', 'verticalAlign': 'middle','margin-top':20}), #({,'border':'2px green solid'}),
    ],
    ),
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # print("pathname: ", pathname)
    if pathname == '/pages/pca':
        return pca.layout
    elif pathname == '/pages/methods':
        return methods.layout
    elif pathname == '/pages/datatable':
        return datatable.layout
    elif pathname == '/pages/clustering':
        return clustering.layout
    elif pathname == '/pages/clustering2':
        return clustering2.layout
    elif pathname == '/pages/clustering3':
        return clustering3.layout
    elif pathname == '/pages/timeseries':
        return timeseries.layout
    elif pathname == '/pages/logistic':
        return logistic.layout
    elif pathname == '/pages/paper':
        return paper.layout
    else:
        return index_page

def main(argv):
    rc = app.run_server(debug=True, processes=1, port=8047)
    #   rc = app.run_server(host='0.0.0.0', debug=False, port=8047)
    if rc:
        print('Error running server')
        sys.exit(-2)

if __name__ == '__main__':
    #   print(f"Arguments count: {len(sys.argv)}")
    #   for iii,arg in enumerate(sys.argv):
    #       print(f"Arguments {iii:>6}: {arg}")
    main(sys.argv[1:])
