from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app


layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Agglomerative Hierarchical Clustering: 74 Biosets'),
    ),
    html.Div([
        dcc.Markdown('''
        Two-way agglomerative hierarchical clustering heatmap of 74 SARSCoV-1 biosets
        using differential RNA Expression based directional gene scores to calculate
        Euclidian distance and nearest neighbors cluster agglomeration.  
        > Vertical axis shows all gene names included in the analysis. Genes with data at any four of the five timepoints were selected.  
        > Horizontal axis shows all bioset IDs.   
        > Horizonal color bars above the heatmap represent the features- days post-infection, viral variant, host age and viral dose (from top to bottom).  
        > Heatmap cells are colored based on direction and magnitude of the gene score for the related bioset.  
        > Hover over a cell to trigger a hover box revealing more information including the gene score.  
        > Hovering also reveals a Plotly Dash control bar in the upper right-hand side with zoom and download options.  
        > Left-mouse click, drag and then release to select an area to zoom.
        ''')
    ]),
    html.Br(),
    html.Center(
        html.Iframe(
                    src=app.get_asset_url("74bs_R4v2_2_hm.html"),
                    style={'height': '1000px', 'width':'98%'},
                   ),
    ),
    html.Br(),
    html.Div(id='clustering-display-value'),
    html.Br(),
    html.Div(
        html.Img(src=app.get_asset_url('heatmapLegend.png'), style={'height':'50%', 'width':'50%'}, id='triarrow'),
        style={'textAlign':'center'}
    ),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])


