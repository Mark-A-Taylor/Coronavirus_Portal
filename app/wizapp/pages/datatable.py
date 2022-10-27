from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash import dash_table
import numpy as np

from app import app
import calcs

param_dict = calcs.fixed_params()
[dfw, dfw_nozeros, gene_ts_mean, gene_ts_std, bioset_chars] = calcs.calc_data(param_dict)


layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.H3('Data: 74 SARS-CoV-1 lung infected vs mock infected biosets'),
    html.Div([
        dcc.Markdown(''' 
        The 74 biosets are characterized below including time post-infection, mouse age category,
        viral strain and dose magnitude.    
        > There are 74 biosets to explore using click-sort on the table columns.  
        > The 'filter data' functionality is available in all of the data columns.  
        > Input a string in string column to do a case sensitive search, e.g. 'MA15e' in the 'Viral Strain' column.  
        > Mathematical operators '<', '>', '<=', '>=' and '!=' work in numeric columns, e.g. '>1'
            in the 'Day Post-Infection' column.   
        > More information regarding interactivity in the data table can be found on the
            [Dash Plotly website](https://dash.plotly.com/datatable/interactivity).    
        > Select 'Export' to download the visible data.  
        > Select 'Download Full Dataset' to download all the data.  
        '''),
    ]),

    html.Div(
        dash_table.DataTable(
            id='datatable',
            columns=[
                #{"name": i, "id": i} for i in sorted(gene_ts_mean.columns)
                {"name": i, "id": i} for i in bioset_chars.columns
            ],
            page_current=0,
            page_size=15,
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
        className='six columns',
        style={'display':'inline-block','width':'95%','vertical-align':'start', 'overflowX':'scroll'},
    ),
    html.Br(),
    html.Div([
        html.Button("Download Full Dataset", id="btn-download-txt"),
        dcc.Download(id="download-text")
    ]),
    html.Br(),
    html.Br(),
    dcc.Link('Return to Index', href='/'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
])


@app.callback(
    Output('datatable', "data"),
    [Input('datatable', "page_current"),
     Input('datatable', "page_size"),
     Input('datatable', "sort_by"),
     Input('datatable', "filter_query"),
     ])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')

    dff = bioset_chars

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
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(dfw_nozeros.to_csv, "74biosets.csv")
