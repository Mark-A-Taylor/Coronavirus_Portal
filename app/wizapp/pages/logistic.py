from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output
import pandas as pd 
from app import app
import plotly.express as px
## data 
df_weight = pd.read_csv('data/bootstrap_features_selected.csv')


## fig 
fig = px.bar(
    df_weight.sort_values('avg_weight',ascending = False),
    x="avg_weight",
    y='gene',
    error_x= 'std_weight',
    color = "avg_weight",
    hover_data=["counts","std_weight"],
    color_continuous_scale='prgn_r',
    template='plotly_white'
) 


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
        style = {"width":"100%"},
        children=[
            html.Tr( [
                html.Th('Training Statistics',style = {"width":"30%"}), 
                html.Th("Gene Weight",style = {"width":"30%"}), 
                html.Th('Heatmap',style = {"width":"40%"})] ),            
            html.Tr(
                children=[                       
                    html.Td(
                        html.Img(
                            src = app.get_asset_url('fig7a_bootstrap.svg'),
                            style = {"width":"100%"}
                        )
                    ),
                    html.Td(  
                        html.Div(
                            dcc.Graph(figure=fig)
                        )          
                    ),                    
                    html.Td(
                        html.Img(
                            src = app.get_asset_url('fig7b.svg'),
                            style = {"width":"100%"}
                        )
                    )
                ])
    ]),
    html.Br(),
    html.Div(id='logistic-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])

