import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
from sklearn.decomposition import PCA

file_folder = '../seed/data/'
# TODO: compute means on-the-fly from full bioset info
# TODO: move to latest version of data
# TODO: compute/add SDevs to time series charts
df = pd.read_csv(file_folder + 'Means.csv')
df3 = pd.read_csv(file_folder + '74biosets_abridged.csv')

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    html.H1('Index:'),
    dcc.Link('Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Clustering', href='/CA'),
])

TSA_layout = html.Div([
    html.H1('Time Series'),
    html.Br(),
    html.Br(),
    dcc.Link('Go to Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Go to Clustering', href='/CA'),
    html.Br(),
    dcc.Link('Back to Index', href='/'),
    html.Br(),
    html.Br(),

    html.Div(
        dash_table.DataTable(
            id='table-paging-with-graph',
            columns=[
                {"name": i, "id": i} for i in sorted(df.columns)
            ],
            page_current=0,
            page_size=20,
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
            #page_size= 10,
        ),
        style={'height': 750, 'overflowY': 'scroll'},
        className='six columns'
    ),
    html.Div(
        id='table-paging-with-graph-container',
        className="five columns"
    ),

    #########
    # TODO: add the breakout charts
    # TODO: move this slider with breakout charts to another page?
    # html.Div(
    #     [
    #         dcc.Slider(
    #             id='meta-slider',
    #             min=0,
    #             max=10,
    #             step=None,
    #             marks={
    #                 0: 'days',
    #                 3: 'strain',
    #                 5: 'dose',
    #                 7: 'age'
    #             },
    #             value=3
    #         )
    #     ]
    # ),
    #########
])


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value
    return [None] * 3


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('table-paging-with-graph', "filter_query")])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')

    dff = df

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            # m = re.search(r'\s+OR\s+',filter_value)
            # if (m):
            # else:
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        else:
            dff = dff.loc[dff["Gene"].str.contains("Ifn")]

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
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)
    layout = go.Layout(title='Exp Plot', xaxis=dict(title='Day'), yaxis=dict(title='(expression)'), width=1200,
                       height=800)
    # see https://plotly.com/python/px-arguments/ for more options
    fig = go.Figure(layout=layout)

    x_axis = ["Mean(0.5)", "Mean(1)", "Mean(2)", "Mean(4)", "Mean(7)"]

    for row in rows:
        i = 1
        gene = "x"
        y_series = []
        for key, value in row.items():
            # print (key, value)
            if (i == 1):
                gene = value
            else:
                y_series.append(value)
            i = i + 1
        exp_data = go.Scatter(x=x_axis, y=y_series)
        fig.add_trace(go.Scatter(exp_data, name=gene, textposition="top center"))

    #    features = []
    #    i = 4
    #    while i < len(df3.columns):
    #        features.append(df3.columns[i])
    #        i = i + 1
    #    X = df3[features]
    #    pca = PCA(n_components=3)
    #    components = pca.fit_transform(X)
    #    total_var = pca.explained_variance_ratio_.sum() * 100
    #    labels = {'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
    #    # labels['color'] = 'days post-infection'
    #    # value =  3
    #    meta = 0
    #    if meta == 0:
    #        colorby = 'Day Post-Infection'
    #        labels['color'] = 'DPI'
    #    elif meta == 3:
    #        colorby = 'SARS Strain'
    #        labels['color'] = 'Strain'
    #    elif meta == 5:
    #        colorby = 'Viral Dose (PFU)'
    #        labels['color'] = 'Dose'
    #    elif meta == 7:
    #        colorby = 'Age Group'
    #        labels['color'] = 'Age Group'
    #
    #    print("meta: " + str(meta))
    #    print(colorby)
    #    fig3 = px.scatter_3d(
    #        components, x=0, y=1, z=2, color=df3[colorby],
    #        title=f'Total Explained Variance: {total_var:.2f}%',
    #        labels=labels, width=1200, height=800
    #    )

    return html.Div(
        [
            dcc.Graph(
                id='time-series',
                figure=fig
            ),
        ]

    )


PCA_layout = html.Div([
    html.H1('Principal Components'),
    html.Br(),
    html.Br(),
    html.Div(id='PCA-content'),
    html.Br(),
    dcc.Link('Go to Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Go to Clustering', href='/CA'),
    html.Br(),
    dcc.Link('Back to Index', href='/'),
    html.Br(),
    html.Br(),

    html.Div(
        id='pca-graph-container',
        className="four columns"
    ),
    html.Div(
        [
            dcc.Slider(
                id='meta-slider',
                min=0,
                max=10,
                step=None,
                marks={
                    0: 'days',
                    3: 'strain',
                    5: 'dose',
                    7: 'age'
                },
                value=3
            )
        ]
    ),
])


@app.callback(
    Output('pca-graph-container', "children"),
    [Input('meta-slider', "value")])
def update_pca(meta):
    features = []
    i = 4
    while i < len(df3.columns):
        features.append(df3.columns[i])
        i = i + 1
    X = df3[features]
    pca = PCA(n_components=3)
    components = pca.fit_transform(X)
    total_var = pca.explained_variance_ratio_.sum() * 100
    labels = {'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
    # labels['color'] = 'days post-infection'
    # value =  3
    if meta == 0:
        colorby = 'Day Post-Infection'
        labels['color'] = 'DPI'
    elif meta == 3:
        colorby = 'SARS Strain'
        labels['color'] = 'Strain'
    elif meta == 5:
        colorby = 'Viral Dose (PFU)'
        labels['color'] = 'Dose'
    elif meta == 7:
        colorby = 'Age Group'
        labels['color'] = 'Age Group'

    print("meta: " + str(meta))
    print(colorby)
    fig3 = px.scatter_3d(
        components, x=0, y=1, z=2, color=df3[colorby],
        title=f'Total Explained Variance: {total_var:.2f}%',
        labels=labels, width=1200, height=800
    )

    return html.Div(
        [
           dcc.Graph(
               id='pca',
               figure=fig3
           )
        ]
    )

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


CA_layout = html.Div([
    html.H1('Clustering'),

    html.Div(id='CA-content'),
    html.Br(),
    dcc.Link('Go to Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Go to Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Back to Index', href='/'),
    html.Br(),
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/TSA':
        return TSA_layout
    elif pathname == '/PCA':
        return PCA_layout
    elif pathname == '/CA':
        return CA_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8049,debug=True)
