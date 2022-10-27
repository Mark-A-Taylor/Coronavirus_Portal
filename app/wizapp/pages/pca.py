from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import inspect

# unique to this application
from app import app
import calcs

layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.H3('Principal Components:'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='pca-dropdown2',
                options=[
                    {'label': 'Color: {}'.format(i), 'value': i} for i in [
                        'Day Post-Infection', 'Viral Strain', 'Viral Dose', 'Host Age Category','None',
                    ]
                ],
                value='Viral Strain'
            ),
        ], style={'display':'inline-block','verticalAlign':'middle','width':'20%','marginLeft':2, 'marginRight':2}),
        html.Div([
            dcc.Dropdown(
                id='pca-dropdown1',
                options=[
                    {'label': 'Shape: {}'.format(i), 'value': i} for i in [
                        'Day Post-Infection', 'Viral Strain', 'Viral Dose', 'Host Age Category','None',
                    ]
                ],
                value='Viral Dose'
            ),
        ], style={'display':'inline-block','verticalAlign':'middle','width':'20%','marginLeft':2, 'marginRight':2}),
        html.Div([
            dcc.Dropdown(
                id='pca-dropdown3',
                options=[
                    #{'label': 'Normalization: {}'.format(i), 'value': i} for i in [
                    #    'None', 'Center', 'Standardize',  # IGNORE this option: 'Normalize'
                    #]
                    {'label': 'Preprocess: None', 'value': 'None','title':'No preprocessing of features.'},
                    {'label': 'Preprocess: Center', 'value': 'Center', 'title':'Features centered to zero mean.'},
                    {'label': 'Preprocess: Standardize', 'value': 'Standardize',
                         'title':'Features centered to zero mean and scaled to unit variance.'},
                ],
                value='None'
            ),
        ], style={'display':'inline-block','verticalAlign':'middle','width':'25%','marginLeft':2, 'marginRight':2}),
        html.Div([
            dcc.Dropdown(
                id='pca-ncomps',
                options=[
                    {'label': '#PCs: 2', 'value': '2', 'title': 'Plot projection using top two principal components.'},
                    {'label': '#PCs: 3', 'value': '3', 'title': 'Plot projection using top three principal components.'},
                ],
            value='3'
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'middle', 'width': '15%', 'marginLeft': 2,
                  'marginRight': 2}),

    ]),
    html.Br(),
    html.Center([
        html.Div(id='pca-display-value'),
    ]),
    dcc.Link('Return to Index', href='/')
])

@app.callback(
    Output('pca-display-value', 'children'),
    Input('pca-dropdown1', 'value'),
    Input('pca-dropdown2', 'value'),
    Input('pca-dropdown3', 'value'),
    Input('pca-ncomps', 'value'),
    )
def update_pca(shape_var, color_var, mode, str_ncomps):
    fname = inspect.stack()[0][3]
    param_dict = calcs.fixed_params()
    ncomps = int(str_ncomps)
    [dfw, dfw_nozeros, gene_ts_mean, gene_ts_std, bioset_chars] = calcs.calc_data(param_dict)
    gene_features = calcs.extract_genexp_features(dfw_nozeros, param_dict)
    [nsample,nfeature] = gene_features.shape
    [rc, explained_variance, explained_variance_ratio, num_components, projection] = calcs.calc_pcas(
        param_dict, gene_features, nsample, nfeature, normalization=mode,ncomps=ncomps)
    graph_data = pd.DataFrame(projection)

    # title_figPCA = f'Total Explained Variance: {total_var:.1f}%'
    x_figPCA = f'PC1: ({explained_variance_ratio[0] * 100:.1f}%)'
    y_figPCA = f'PC2: ({explained_variance_ratio[1] * 100:.1f}%)'
    if (ncomps < 3):
        graph_data.columns = ['PC1','PC2']
        labels = {'PC1': x_figPCA, 'PC2': y_figPCA}
    else:
        z_figPCA = f'PC3: ({explained_variance_ratio[2] * 100:.1f}%)'
        graph_data.columns = ['PC1','PC2','PC3']
        labels = {'PC1': x_figPCA, 'PC2': y_figPCA, 'PC3': z_figPCA}

    hover_cols=['Day Post-Infection',
                #'Species',
                #'GEO ID, link',
                #'Study name',
                #'Bioset name',
                #'Test Samples',
                #'Control Samples',
                #'Feature Size',
                'Article PubMed ID',
                'Viral Strain',
                #'SARS-CoV Strain',
                'Viral Dose',
                #'Viral Dose (PFUs)',
                #'Viral Severity',
                #'Sample Source (strain, cell)',
                #'Host Mouse Strain',
                #'Sex',
                #'Host Age',
                'Host Age Category',
                #'Technology',
                #'Lab',
                ]
    hover_data = dfw_nozeros[hover_cols]
    graph_data2 = pd.concat([graph_data,hover_data],axis=1)
    shape_input = None
    if shape_var != 'None':
        print("shape_var: " + str(shape_var))
        #print("type shape_var: ",type(dfw_nozeros[shape_var]))
        labels['symbol'] = shape_var
        shape_input = dfw_nozeros[shape_var].astype(str)
    color_input = None
    if color_var != 'None':
        print("color_var: " + str(color_var))
        #print("type color_var: ",type(dfw_nozeros[color_var]))
        labels['color'] = color_var
        color_input = dfw_nozeros[color_var].astype(str)

    # hardwire the symbols to be used:
    symbol_seq = ['circle','square','diamond','circle-open','square-open','diamond-open']
    if (ncomps < 3):
        fig_pca = px.scatter(
            data_frame=graph_data2, x='PC1', y='PC2',
            color=color_input,
            symbol=shape_input,
            symbol_sequence=symbol_seq,
            labels=labels,  width=900, height=600,
            opacity=0.75,
            hover_data=hover_cols,
        )
        fig_pca.update_layout(
            legend=dict(yanchor="top",y=.95,xanchor="left",x=1.05),
        )
    else:
        fig_pca = px.scatter_3d(
            graph_data2, x='PC1', y='PC2', z='PC3',
            color=color_input,
            symbol=shape_input,
            symbol_sequence=symbol_seq,
            # title=title_figPCA ,
            labels=labels,  width=900, height=600,
            opacity=0.75,
            #hover_name='GEO ID, link',
            hover_data=hover_cols,
        )
        fig_pca.update_layout(
            margin=dict(l=0,r=0,b=0,t=0),
            legend=dict(yanchor="top",y=.95,xanchor="left",x=1.05),
        )
        #   fig_pca.update_traces(
        #           marker=dict(size=12,line=dict(width=2, color='grey')),
        #           selector=dict(mode='markers'),
        #   )

    return html.Div(
        [
           dcc.Graph(
               id='pca',
               figure=fig_pca
           )
        ]
    )
    #    return 'You have selected "{}"'.format(value)

