from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
import pandas as pd
#   import glob

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
        
        Code for generating this heatmap is provided [here](https://github.com/Mark-A-Taylor/Coronavirus_Portal/tree/cv/74_biosets) for
        readers to explore the data with the Interactive Complex Heatmap R Shiny application,
        which allows for data sub-setting and additional navigation features.
        ''')
    ]),
    html.Br(),
    html.Div([
        html.Button("Download Dataset (post clustering)", id="btn-download-cluster"),
        dcc.Download(id="download-cluster")
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

@app.callback(
    Output("download-cluster", "data"),
    Input("btn-download-cluster", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
   input_file_folder1 = '../../74_biosets/'
   input_file_name1 = "74bs_post_cluster_data.csv"
   filepath_name1 = input_file_folder1 + input_file_name1
   #   for filename in glob.iglob(input_file_folder1+'**/**',recursive=True):
   #       print(filename)
   seventyfour = pd.read_csv(filepath_name1, sep=',', lineterminator='\n')
   return dcc.send_data_frame(seventyfour.to_csv, "74_post_cluster.csv")


