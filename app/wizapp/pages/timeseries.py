from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
import numpy as np

from app import app
import calcs

param_dict = calcs.fixed_params()
[dfw, dfw_nozeros, gene_ts_mean, gene_ts_std, bioset_chars] = calcs.calc_data(param_dict)

layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.H3('5 Temporal Meta-Signature Gene Scores'),
    html.Div([
        dcc.Markdown('''
        Time series of normalized gene expression scores averaged across 74 Biosets for 0.5, 1, 2, 4 and 7 Days Post-Infection (DPI).  
        > There are ~10,000 genes to explore using click-sort on the table columns.  
        > Mouse click on graph legend to toggle to suppress/reveal the time series for select genes.  
        > Hover over a graph data points to trigger a hover box revealing more information regarding that data point.  
        > The 'filter data' functionality is available in all of the data columns.  
        > Input a string in 'Gene' column to do a case sensitive search by gene mnemonic, e.g. 'Ifna' or 'fna' to find interferons.  
        > Mathematical operators '<', '>', '<=', '>=' and '!=' work in numeric columns, e.g. '>95' in the '2 DPI' column to find genes over 95.  
        > More information regarding interactivity in the data table can be found on the
            [Dash Plotly website](https://dash.plotly.com/datatable/interactivity).   
        > Select 'Export' to download the visible data.  
        > Select 'Download Full Dataset' to download all the data.  
        '''),
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='ts-dropdown',
                options=[
                    {'label': 'Error Bars: {}'.format(i), 'value': i} for i in [ 'On','Off']
                ],
                value='Off'
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'middle', 'width': '20%', 'marginLeft': 2,
                  'marginRight': 2}),
        html.Div([
            dcc.Dropdown(
                id='ts-dropdown2',
                options=[
                    {'label': 'Symbol Size: {}'.format(i), 'value': i} for i in [ '1','2','5','10']
                ],
                value='2'
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'middle', 'width': '20%', 'marginLeft': 2,
                  'marginRight': 2}),
    ]),

    html.Div([
        html.Div(
            id='table-paging-with-graph-container',
            className="five columns",
            style={'display':'inline-block','width':'55%','vertical-align':'start'},
        ),
        html.Div(
            html.Div([
                dash_table.DataTable(
                    id='table-paging-with-graph',
                    columns=[
                        #{"name": i, "id": i} for i in sorted(gene_ts_mean.columns)
                        {"name": i, "id": i} for i in gene_ts_mean.columns
                    ],
                    page_current=0,
                    page_size=10,
                    page_action='custom',
                    filter_action='custom',
                    filter_query='',
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    editable=True,
                    #filter_action="native",
                    #sort_action="native",
                    #sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    #page_action="native",
                    #page_current= 0,
                    export_format="csv",
                ),
                #style={'height': 400, 'overflowY': 'scroll'},
                html.Div([
                    html.Button("Download Full Dataset", id="btn2-download-txt"),
                    dcc.Download(id="download-text2")
                ]),
            ]),
            className='six columns',
            style={'display': 'inline-block', 'width': '45%', 'vertical-align': 'start'},
        ),
    ]),
    html.Br(),
    dcc.Link('Return to Index', href='/'),
    html.Br(),
    html.Br(),

])


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('table-paging-with-graph', "filter_query"),
     Input('ts-dropdown', 'value'),
     Input('ts-dropdown2', 'value'),
     ])
def update_table(page_current, page_size, sort_by, filter, error_bar, symbol_size  ):
    filtering_expressions = filter.split(' && ')

    dff = gene_ts_mean

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = calcs.split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff[np.char.find( dff[col_name].values.astype(str), str(filter_value) ) > -1]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        #else:
            # DEFAULT view:
            #   dff = dff.loc[dff["Gene"].str.contains("Ifn")]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return dff.iloc[
           page_current * page_size: (page_current + 1) * page_size
           ].to_dict('records')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data"),
     Input('ts-dropdown', 'value'),
     Input('ts-dropdown2', 'value'),
     ])
def update_graph(rows, error_bar, symbol_size):
    dff = pd.DataFrame(rows)
    DPI_COL = param_dict['DPI_COL']
    layout = go.Layout(
            #title='Select gene scores vs days post infection:',  
            xaxis=dict(title=DPI_COL),
            yaxis=dict(title='(expression)'),
            #width=600, height=400
            )
    # see https://plotly.com/python/px-arguments/ for more options
    # TODO:  https://plotly.com/python/error-bars/ for error bars
    fig = go.Figure(layout=layout)
    x_axis = ["0.5 DPI", "1 DPI", "2 DPI", "4 DPI", "7 DPI"]
    std_cols = ['Std(0.5)','Std(1)','Std(2)','Std(4)','Std(7)']
    for row in rows:
        i = 1
        gene = row['Gene']
        y_series = []
        for key, value in row.items():
            # print (key, value)
            if (i == 1):
                gene = value
            else:
                y_series.append(value)
            i = i + 1
        std_series = []
        for val in std_cols:
            std_series.append( gene_ts_std.loc[ gene_ts_std['Gene'] == gene, val] )
        if error_bar == 'On':
            exp_data = go.Scatter(x=x_axis, y=y_series, error_y=dict(array=std_series,visible=True))
        else:
            exp_data = go.Scatter(x=x_axis, y=y_series)
        info_text = 'Gene:'+gene
        fig.add_trace(go.Scatter( exp_data,
                                  name=gene,
                                  textposition="top center",
                                  marker_size=int(symbol_size),
                                  marker_line_width=1,
                                  text=info_text,
                                  ))
    return html.Div(
        [
            dcc.Graph(
                id='time-series',
                figure=fig,
                # style={'width':'80vw','height':'50vh'}
            ),
        ]

    )

@app.callback(
    Output("download-text2", "data"),
    Input("btn2-download-txt", "n_clicks"),
    prevent_initial_call=True,
)
def func2(n_clicks):
    return dcc.send_data_frame(gene_ts_mean.to_csv, "gene_timeseries.csv")
