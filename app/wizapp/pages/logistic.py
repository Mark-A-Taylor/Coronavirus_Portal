from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output
import pandas as pd 
from app import app

## data 
df_weight = pd.read_csv('data/bootstrap_features_selected.csv')

## layout 
layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Elastic Net Logistic Model with Regularization'),
    ),
    html.Br(),
    html.Table(
        id='bootstrap_stats_table', 
        className='bootstrap_stats_table', 
        children=[
            html.Tr( [html.Th('Training Statistics'), html.Th("Gene Weight"), html.Th('Heatmap')] ),            
            html.Tr(
                children=[                       
                    html.Td(
                        html.Img(
                            src = app.get_asset_url('fig7a_bootstrap.svg')
                        )
                    ),
                    html.Td(            
                        dash_table.DataTable(
                            data = df_weight.to_dict('records'), 
                            columns = [{"name": i, "id": i} for i in df_weight.columns]
                        )),                    
                    html.Td(
                        [html.Img(
                            src = app.get_asset_url('fig7a.svg')
                        ),
                        html.Img(
                            src = app.get_asset_url('fig7b.svg')
                        )]
                    )
                ])
    ]),
    html.Br(),
    html.Div(id='logistic-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])

