from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
import pandas as pd
#   import glob


layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.Center(
        html.H1('Agglomerative Hierarchical Clustering: 5 Temporal Meta-Signatures'),
    ),
    html.Div([
        dcc.Markdown('''
        Two-way agglomerative hierarchical clustering of 5 temporal meta-signature gene profiles
        was performed and revealed 4 distinct gene expression patterns:  
        > (I) genes that are highly up-regulated at 1-2 DPI,  
        > (II) genes highly up-regulated at 4-7 DPI,  
        > (III) genes highly upregulated through most timepoints, and  
        > (IV) genes highly down-regulated through most timepoints.  

        The highest ranking up-regulated gene across all DPI (in pattern III) was Cxcl10
        (C-X-C motif chemokine ligand 10).
        On the other hand, the highest ranking down-regulated gene (in pattern IV) across all DPI
        was Bex2 (brain expressed X-linked 2), while Bex1 and Bex4 trended similarly downward
        over the course of infection.   
        > Vertical axis shows all gene names included in the study.  
        > Horizontal axis shows average expression for each gene at each of the five timepoints.  
        > Heatmap cells are colored based on direction and magnitude of the average gene expression
        at the time point.  
        > Hover over a cell to trigger a hover box revealing more information including the average gene expression.  
        > Hovering also reveals a Plotly Dash control bar in the upper right-hand side with zoom and download options.  
        > Left-mouse click, drag and then release to select an area to zoom.  
        
        Code for generating this heatmap is provided [here](https://github.com/Mark-A-Taylor/Coronavirus_Portal/tree/cv/5_temporal_metasignatures) for
        readers to explore the data with the Interactive Complex Heatmap R Shiny application,
        which allows for data sub-setting and additional navigation features.
        ''')
    ]),
    html.Br(),
    html.Div([
        html.Button("Download Dataset (post clustering)", id="btn-download-cluster2"),
        dcc.Download(id="download-cluster2")
    ]),
    html.Br(),
    html.Center(
        html.Iframe(
                    src=app.get_asset_url("3bv2_ave_dpi_genes_int_hm.html"),
                    style={'height': '1067px', 'width':'100%'},
                   ),
    ),
    html.Br(),
    html.Div(id='clustering2-display-value'),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])

@app.callback(
    Output("download-cluster2", "data"),
    Input("btn-download-cluster2", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    input_file_folder2 = '../../5_temporal_metasignatures/'
    input_file_name2 = "dpi_metaSig_post_cluster_data.csv"
    #   for filename in glob.iglob(input_file_folder2+'**/**',recursive=True):
    #       print(filename)
    filepath_name2 = input_file_folder2 + input_file_name2
    five = pd.read_csv(filepath_name2, sep=',', lineterminator='\n')
    return dcc.send_data_frame(five.to_csv, "5_post_cluster.csv")


