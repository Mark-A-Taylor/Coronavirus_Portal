from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app


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
        ''')
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


