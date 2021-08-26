import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bio as dashbio
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import inspect

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

# global variables
VERBOSITY = 1
NUM_SIG_DIGITS = 2 # digits after the decimal for means and stdevs
DPI_COL = 'Day Post-Infection'
DPI_VALS = [
    0.5
    , 1
    , 2
    , 4
    , 7]
KEY_COLS = [
    'GEO ID, link'
    , 'Day Post-Infection'
    , 'SARS-CoV Strain'
    , 'Host Age Cat'
    , 'Viral Dose']
# HACK - ASSUMES order of genes and continuity w/r/t side-by-side columns
GENE_COL_START = 'March1'
GENE_COL_END = 'Zzz3'


#########################################################
#########################################################
#  Data wrangling routines
def append_meta_data_keys(df):
    # TODO? dynamic input of keys of arbitrary length and type (low priority)
    #   upside: then it would be more portable to other data sets
    # NOTE: Uses global variable KEY_COLS
    fname = inspect.stack()[0][3]
    check_col = 'Count'
    for kkk in KEY_COLS:
        if VERBOSITY > 0:
            print('DEBUG: ',fname,': key_col: ', kkk)
        if kkk not in df:
            print('ERROR: ',fname,': unable to find key column: ',kkk,' in dataframe')
            return False
    df['my_key'] = (df[KEY_COLS[0]] + "_" + df[KEY_COLS[1]].astype(str) +
        "_" + df[KEY_COLS[2]] + "_" + df[KEY_COLS[3]] + "_" + df[KEY_COLS[4]].astype(str))
    # check uniqueness of key
    if check_col not in df:
        print('WARNING: ',fname,': unable to find ',check_col,' and verify uniqueness')
        return False
    table = df.pivot_table(index='my_key', values=check_col, aggfunc=np.sum)
    if table.shape[0] < df.shape[0]:
        print('ERROR: ',fname, ': pivot check for unique key failed.')
        return False
    # on-demand printout of key information
    if VERBOSITY > 0:
        with pd.option_context('display.max_colwidth',200):
            for index,row in dfw_nozeros.iterrows():
                print('DEBUG: ',fname,': ', row['my_key'])
    # all good!
    return True

def extract_genexp_features(df):
    fname = inspect.stack()[0][3]
    icol_start = df.columns.get_loc(GENE_COL_START)
    icol_end = df.columns.get_loc(GENE_COL_END)
    if VERBOSITY > 0:
        print('DEBUG: ',fname, ': GENE_COL_START: ',GENE_COL_START, ', icol_start: ',icol_start)
        print('DEBUG: ',fname, ': GENE_COL_END: ',GENE_COL_END, ', icol_end: ',icol_end)
    # gene expression features for PCA
    gene_features = df.iloc[:, icol_start:icol_end + 1]
    if VERBOSITY > 0:
        print('DEBUG: ',fname, ': shape gene_features: ', gene_features.shape)
    if gene_features.shape[0] < 1:
        print('ERROR: ',fname, ': No features found.')
    return gene_features

def build_gene_time_series(df):
    # strategy: pull list of gene and DPI and populate matrix
    # output matrix will have one row for each gene with a mean and sdev pair for each DPI
    fname = inspect.stack()[0][3]
    gene_features = extract_genexp_features(dfw_nozeros)
    if gene_features.shape[0] < 1:
        print('ERROR: ', __name__, ': Exiting.')
        exit()
    gene_ts_mean = pd.DataFrame()  # results target
    gene_ts_std = pd.DataFrame()  # results target
    for dpi_val in DPI_VALS:
        if VERBOSITY > 0:
            print('DEBUG: ', fname, ': dpi_val:', dpi_val)
        data_set = gene_features[df[DPI_COL] == dpi_val]
        col_name = 'Mean('+str(dpi_val)+')'
        gene_ts_mean[col_name] =  round(data_set.mean(),NUM_SIG_DIGITS)
        col_name = 'Std('+str(dpi_val)+')'
        gene_ts_std[col_name] =  round(data_set.std(),NUM_SIG_DIGITS)
    gene_ts_mean.index.name = 'Gene'
    gene_ts_mean.reset_index(inplace=True)
    gene_ts_std.index.name = 'Gene'
    gene_ts_std.reset_index(inplace=True)
    return [gene_ts_mean, gene_ts_std]

def build_PCA_projection(df):
    fname = inspect.stack()[0][3]
    gene_features = extract_genexp_features(df)
    if gene_features.shape[0] < 1:
        print('ERROR: ', __name__, ': ', fname, ': Exiting.')
        exit()
    pcas = PCA(n_components=3)
    components = pcas.fit_transform(gene_features)
    if VERBOSITY > 0:
        print('gene_features shape: ',gene_features.shape)
        print(f'Total Explained Variance: {pcas.explained_variance_ratio_.sum() * 100:.1f}%')
        print(f'PC1: ({pcas.explained_variance_ratio_[0] * 100:.1f}%)')
        print(f'PC2: ({pcas.explained_variance_ratio_[1] * 100:.1f}%)')
        print(f'PC3: ({pcas.explained_variance_ratio_[2] * 100:.1f}%)')
    return [pcas, components]

# hacky global to minimize reloading data
PROCESS_DATA_BOOL = True
if (PROCESS_DATA_BOOL):
    file_folder = '../data_round4/'
    file_name = "SARS_CoV_Round4v2_74_Biosets_wZero_Time_Point.txt"
    filepath_name = file_folder + file_name
    dfw = pd.read_csv(filepath_name, sep='\t', lineterminator='\n')
    # we also need a copy of the data without the zero time point rows
    dfw_nozeros = (dfw.head(74)).copy(deep=True)
    #
    # add a column 'Count' to allow us to pivot data and get sums for meta data characteristics
    dfw_nozeros['Count'] = 1
    #
    # build/append a unique key for each meta sample for MDA
    if not append_meta_data_keys(dfw_nozeros):
        print('ERROR: ',__name__,': Exiting.' )
        exit()
    #
    # compute time series means & sdevs across meta samples for each gene
    [gene_ts_mean, gene_ts_std] = build_gene_time_series(dfw_nozeros)
    if gene_ts_mean.shape[0] < 1 or gene_ts_std.shape[0] < 1:
        print('ERROR: ', __name__, ': Exiting.')
        exit()
    #
    # PCA and project onto 3 components
    [pcas, components] = build_PCA_projection(dfw_nozeros)
    #       check with previous number in jupyter notebook by including the zero points:
    #       [pcas, components] = build_PCA_projection(dfw)
    if components.shape[0] < 1:
        print('ERROR: ', __name__, ': Exiting.')
    #
    # gene avg features over time for clustergram analysis
    cdf = gene_ts_mean.copy(deep=True)
    cdf.index = cdf['Gene']
    cdf.pop('Gene')
    columns = list(cdf.columns.values)
    rows = list(cdf.index)
    if cdf.shape[0] < 1:
        print('ERROR: ', __name__, ': Exiting.')
        exit()
    columns = list(cdf.columns.values)
    rows = list(cdf.index)


#old_file_folder = '../seed/data/'
#df = pd.read_csv(old_file_folder + 'Means.csv')
#df3 = pd.read_csv(old_file_folder + '74biosets_abridged.csv')

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
    html.H1('Crowdsourcing Temporal Transcriptomic Coronavirus Host Infection Data'),
    html.Br(),
    dcc.Markdown('''
Welcome to this portal to explore the data related to the paper of meta-analysis of
host responses to SARS CoV infection.
'''),

    html.H3('Quick Links:'),
    dcc.Link('Explore Meta Data', href='/EMD'),
    html.Br(),
    dcc.Link('Explore Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Explore Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Explore Clustering', href='/CA'),
    html.Br(),

    dcc.Markdown('''
# Abstract

The emergence of SARS-CoV-2 reawakened the need to rapidly understand the molecular
Acute respiratory infections are among the most common infections globally reported
and often share similar symptoms and clinical markers. A variety of host infection
RNA expression data were used to create temporal, post-infection meta-signatures
that appear to closely emulate SARS-CoV-2 processes. Recapitulation of host effects like
cytokine production, kinase and phosphatase regulation, cell cycle impacts and altered
lipid metabolism are investigated.
The discovery of correlations to hundreds of potentially effective drug treatments is in
part validated by a subset of twenty-four that are in clinical trials to treat COVID-19.
Crowdsourcing large amounts of historical data from related viruses can be leveraged to gain
rapid insight and potentially alleviate morbidity of new outbreaks in record times.

# Introduction

Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2) is an individuum within the beta-coronavirus species ...
'''),
])

EMD_layout = html.Div([
    html.H1('Explore Meta Data'),

    html.Br(),
    dcc.Link('Explore Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Explore Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Explore Clustering', href='/CA'),
    html.Br(),
    dcc.Link('Back to Introduction', href='/'),
    html.Br(),
    html.Div(id='EMD-content'),
])

TSA_layout = html.Div([
    html.H1('Time Series of Normalized Gene Scores Averaged Across 74 Biosets'),
    html.Br(),
    dcc.Link('Explore Meta Data', href='/EMD'),
    html.Br(),
    dcc.Link('Explore Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Explore Clustering', href='/CA'),
    html.Br(),
    dcc.Link('Back to Introduction', href='/'),
    html.Br(),
    html.Br(),

    html.Div(
        dash_table.DataTable(
            id='table-paging-with-graph',
            columns=[
                {"name": i, "id": i} for i in sorted(gene_ts_mean.columns)
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

    dff = gene_ts_mean

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
            # DEFAULT view:
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
    layout = go.Layout(title='Select gene scores vs days post infection:', xaxis=dict(title=DPI_COL)
                       , yaxis=dict(title='(expression)'), width=1200,
                       height=800)
    # see https://plotly.com/python/px-arguments/ for more options
    # TODO:  https://plotly.com/python/error-bars/ for error bars
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
    dcc.Link('Explore Meta Data', href='/EMD'),
    html.Br(),
    dcc.Link('Explore Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Explore Clustering', href='/CA'),
    html.Br(),
    dcc.Link('Back to Introduction', href='/'),
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
                    0: 'DPI',
                    3: 'Viral Strain',
                    5: 'Viral Dose',
                    7: 'Host Age Cat'
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
    fname = inspect.stack()[0][3]
    total_var = pcas.explained_variance_ratio_.sum() * 100
    if VERBOSITY > 0:
        print('DEBUG: ', fname, ': total_var: ', total_var)
    title_figPCA = f'Total Explained Variance: {total_var:.1f}%'
    x_figPCA = f'PC1: ({pcas.explained_variance_ratio_[0] * 100:.1f}%)'
    y_figPCA = f'PC2: ({pcas.explained_variance_ratio_[1] * 100:.1f}%)'
    z_figPCA = f'PC3: ({pcas.explained_variance_ratio_[2] * 100:.1f}%)'
    if meta == 0:
        shapeby = 'Day Post-Infection'
    elif meta == 3:
        shapeby = 'Viral Strain'
    elif meta == 5:
        shapeby = 'Viral Dose'
    elif meta == 7:
        shapeby = 'Host Age Cat'

    # HACK: HARDWIRED color to DPI to control the colormap
    colorby = 'Day Post-Infection'
    labels = {'0': x_figPCA, '1': y_figPCA, '2': z_figPCA, 'color':colorby, 'symbol':shapeby}

    print("meta: " + str(meta))
    print(colorby)
    fig3 = px.scatter_3d(
        components, x=0, y=1, z=2,
        color=dfw_nozeros[colorby],
        symbol=dfw_nozeros[shapeby],
        title=title_figPCA ,
        labels=labels,  width=1200, height=800,
        color_continuous_scale=["red", "green", "blue"]
    )
    fig3.update_layout(coloraxis_colorbar=dict(yanchor="top", y=1., x=1.25,
                                                 ticks="outside"
                                                 , ticksuffix=" days"
                                                 )
                         )

    return html.Div(
        [
           dcc.Graph(
               id='pca',
               figure=fig3
           )
        ]
    )


CA_layout = html.Div([
    html.H1('Clustering'),
    html.Div(id='CA-content'),
    html.Br(),
    dcc.Link('Explore Meta Data', href='/EMD'),
    html.Br(),
    dcc.Link('Explore Time Series', href='/TSA'),
    html.Br(),
    dcc.Link('Explore Principal Components', href='/PCA'),
    html.Br(),
    dcc.Link('Back to Introduction', href='/'),
    html.Br(),
    html.Br(),

#    html.Div(dcc.Graph(figure=dashbio.Clustergram(
#        data=cdf.loc[rows].values,
#        column_labels=columns,
#        row_labels=rows,
#        color_threshold={
#            'row': 250,
#            'col': 700
#        },
#        hidden_labels='row',
#        height=800,
#        width=700
#        , color_map=[
#            [0.0, '#0099ff'],  # blue
#            [0.5, '#000000'],  # black
#            [1.0, '#ffff00']  # yellow
#        ]
#    )))
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/EMD':
        return EMD_layout
    elif pathname == '/TSA':
        return TSA_layout
    elif pathname == '/PCA':
        return PCA_layout
    elif pathname == '/CA':
        return CA_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here



if __name__ == '__main__':
    print("running on host 127.0.0.1, port 8047")
    app.run_server(host='127.0.0.1', port=8047,debug=False)
