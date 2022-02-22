from dash import dcc
from dash import html
#from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.Div([dcc.Link('Return to Index', href='/')],style={'text-align':'right'}),
    html.H3('Methods'),
    # :whtml.Br(),
    html.Div([
    dcc.Markdown('''
Illumina's BaseSpace Correlation Engine (Kupershmidt et al., 2010) (BSCE, previously known as NextBio) was used to facilitate the aggregation and mining of coronavirus host infection transcriptome data for two main reasons. BSCE contains over 21,500 omic-scale Curated Studies with over 132,000 experimental comparison results (hereafter called biosets). Consistent curation practices increases the inclusion of high quality datasets for analysis and improves the resulting interpretations. Curated Studies in BSCE are processed in standard, platform-specific pipelines to generate gene sets and measures. For each study, available Test group versus Control group results plus experimental metadata are generated. Second, BSCE has robust data-driven correlation, aggregation, and machine learning applications to exploit the consistent processing and curation of omic-scale (Barrett et al., 2013) Studies from international public repositories, including US-NCBI's Gene Expression Omnibus (Barrett et al., 2013) and the Short Read Archive (Leinonen et al., 2011) EMBL-EBI's Array Express (Athar et al., 2019), US-NIEHS's NTP Chemical Effects in Biological Systems (CEBS) (Gwinn et al., 2020), and Japan's Toxicogenomics Project-Genomics Assisted Toxicity Evaluation System (TG-GATES) (Igarashi et al., 2015).  

   **Systematic Review of Omic-scale Studies and Experimental Designs.**  

A search of BSCE identified 44 Curated Studies with a total of 447 Biosets querying the term "Coronavirus". The Biosets covered a wide range of experimental designs across an array of viral species, viral individuum variants, viral dose, post-infection duration, host organism, host tissue, host sex, host age, gene knock out models, cell line models, compound treatments and technology platforms. Study and experimental bioset details were hand curated from BSCE, the GEO entry and primary articles.  

**RNA Expression Analysis.**  

Threshold filters between test (e.g., virus infected) and control (e.g., mock infection) conditions were applied to log2 scale RNA expression data. Genes with both mean normalized test and control intensities less than the 20th percentile of the combined normalized signal intensities were removed. A parametric Welch t-test, where variances are not assumed equal, is calculated and genes with a p-value > 0.05 were removed. An additional filter removes genes with non-log2 absolute fold change < 1.2 to generate the final list of differentially expressed genes in a bioset. The parametrically determined gene list is set to non-parametric ranks by assigning the gene with the highest absolute fold change the highest rank of 1 and genes descending by absolute fold change are numbered down the ordinal ranks. Bioset-Bioset correlations are done based on the ranks using the Running Fisher algorithm (Kupershmidt et al., 2010). BSCE calculates normalized, bioset-specific gene scores that considers the absolute fold change rank, the number of genes passing threshold filters and the number of genes measured by the platform on a 100 to 0 scale. A positive or negative sign was appended to gene scores based on the fold change direction to generate values ranging from -100 to +100, hereforth called directional gene score.  

 RNA expression analysis of SARS-CoV-1 lung infected versus mock infected control used biosets from 4 mammalian species and 9 beta-coronavirus variants, encompassing 19 Curated Studies with a total of 97 Biosets \[Mus musculus - mouse (n=85), Macaca fascicularis - cynomolgus macaques (n=5), Mustela putorius furo - ferret (n=5) and in Homo sapiens - human cells (n=2)\]. Biosets covered 48 early, 42 mid and 7 late stage infection results \[0.5, 1, 2, 3, 4, 5, 7, 14, 21 and 28 days post-infection (dpi)\]. Beta-coronavirus variants included SARS-CoV-MA15, SARS-CoV-MA15e, SARS-CoV-MA15g, SARS-CoV-TOR-2, SARS-CoV-GZ02, SARS-CoV-HC-SZ-6103, SARS-CoV-ic, SARS-CoV-Urbani, and SARS-CoV-2 USA-WA1/2020 (NR-52281). Technology Platforms included \[Agilent-014868 Whole Mouse Genome Microarray 4x44K G4122F, Affymetrix Mouse Genome 430 2.0, Affymetrix Canine Genome 2.0 Array, Array Affymetrix Rhesus Macaque Genome Array, Illumina NextSeq 500\]. We filtered the time course based on the number of biosets available per dpi; those with less than 3 biosets were excluded to minimize skewing from an overreaching but underrepresented variable set. This left 74 SARS-CoV-1 lung infected versus mock infected Biosets in mouse at 0.5, 1, 2, 4, and 7 dpi comprised of 299 experimental and 239 control animals as the focus for the current study. Metadata and gene expression matrix are in Supplemental Table 1 of the paper.  

**Generation of Temporal Meta-Signatures.**  

The 74 Biosets spanned i) five post-infection time points, ii) 3 host age groups, iii) 3 host strains, iv) 5 viral variants, and v) 4 magnitudes of viral dose. Age groups were divided into young mice (10 wkseek), adult (20 to 23 weeks), and aged (52 weeks). To the best of our knowledge all were female. Mus musculus strains included BALB/c, 129/S6/SvEv and C57BL/6NJ. The most commonly used MA15 variant induces more severe reactions in mice than MA15g, MA15e or the ic (infectious clone) and wildtype TOR-2 variants (Roberts et al., 2007, Rockx et al., 2009). Intranasal infection dose levels included 100, 1,000, 10,000, 22,000 and 100,000 viral plaque forming units (pfu).   

The BSCE Meta-Analysis application takes an input of a collection of Biosets and outputs a table with the top 5,000 genes ranked in rows by highest sum of the normalized gene scores with bioset-specific fold change and p-values in columns. Meta-Analysis was run separately in sets for 6 Biosets at 0.5 dpi, 15 Biosets at 1 dpi, 19 Biosets at 2 dpi, 19 Biosets at 4 dpi and 15 Biosets at 7 dpi. The average of the -100 to +100 scaled RNA expression  directional gene score values was taken for each gene score in the set and used as the meta-signature value for each of the five post-infection time points, hereforth called temporal score(s). Meta-signatures were aligned into a matrix to form 10,564 gene-specific time vectors following host response to SARS-CoV-1 infection in mouse lung (Supplemental Table 2 of the paper).  

**Unsupervised Machine Learning Analyses.**  

Principal Component Analysis of the 74 Biosets was generated using Qlucore Omics Explorer software v3.6, Sweden and custom Plotly scripts (Montreal, Quebec, Canada). Venn diagram was generated using the Gent University Bioinformatics and Evolutionary Genomics application at http://bioinformatics.psb.ugent.be/webtools/Venn/. Profile Charts of Meta-Signature genes were generated using (JMP Pro 15.0 (SAS).  

Agglomerative hierarchical clustering was performed by generating a static heatmap using the native R heatmap function "heatmap.2", which orders features based on Euclidian distance and nearest neighbors agglomeration, no additional normalization was performed, and no parameters adjusted. Row and column dendrograms were isolated from the static heatmap and applied to third party heatmap packages "heatmaply" and "InteractiveComplexHeatmap" to generate interactive heatmaps.  

The BSCE Pathway Enrichment application was used to correlate and rank the temporal meta-signatures to functional concepts derived from Gene Ontology (Consortium, 2004). Biogroup concepts with a minimum of 10 and a maximum of 750 genes were used, thereby eliminating minor concepts and those with little specificity.  

Network Analysis was performed using STRING, Protein-Protein Interaction Networks and Functional Enrichment Analysis at https://string-db.org (Szklarczyk et al., 2019) and Pathway Studio (Elsevier B.V., Amsterdam, Netherlands). Other gene function analysis were performed using the WEB-based GEne SeT AnaLysis Toolkit software (http://www.webgestalt.org/)(Liao et al., 2019, Wang et al., 2017).  

**Supervised Machine Learning Analyses.**  

Binary elastic-net logistic regression combined with bootstrapping was applied to derive predictive models and robust coefficients of the genes in making temporal predictions (Barretina et al., 2012, Zou and Hastie, 2005). Given observations of distinctive early versus late activities, samples were grouped as either early \[0.5, 1, 2 dpi\] or late \[4, 7 dpi\] to derive a small set of genes that could predict the stage of SARS-CoV-1 infection. Each bootstrap split the data into different training and testing sets with a ratio 4:1 using the "train_test_split" function from sklearn with "stratify=y" and a random seed generated using "randrange" function. 100 different splits were generated by repeatedly calling "randrange" function in "train_test_split" and any duplicated splits were programmatically removed. For each split, a combination of 3-fold cross-validation and hyperparameters search was performed using the "GridSearchCV" function with "cv=3" from sklearn on the training set. The two hyperparameters, "C" and "l1_ratio", were the targets of the grid search. The "C" parameter is the inverse of lambda, which controls the overall strength of the regulation term in elastic net, and was set to 1e-4, 1e-3, 1e-2, 1e-1, 1 and 10. The "l1_ratio" controls the ratio between L1 and L2 regulation terms, which was 0.2, 0.4, 0.6, 0.8 and 1. The combination of these two hyperparameters with the lowest cross validation error was selected and used to derive the coefficient for each gene in the model to predict the early or late stage for each sample in validation set and test set. The validation accuracy was reported as training accuracy and the test accuracy was calculated by using "accuracy_score" function from sklearn by using the best model on testing set. The coefficients of the genes from these 100 bootstraps were summarized and only genes with at least 90 of 100 bootstraps with a nonzero weight were reported in the final list with the average coefficient and standard deviation.  

**Correlations to Compound Treatments, Gene Perturbations and Diseases.**  

The five temporal meta-signatures were imported into BSCE as Biosets and queried in the BSCE Pharmaco, Knockout, Knockdown and Disease Atlas applications. Bioset queries made against the entire repository yield a Bioset-Bioset correlation rank ordered list. BSCE Biosets are tagged with concept terms that capture sample and experimental details, like compound treatments, genetic perturbations and phenotypes. A machine learning categorization process assesses the rank of correlations to the tagged concept term results into Pharmaco, Knockdown and Disease Atlases using relevant tag types and strength of contributing Bioset correlations (See Supplemental Text BSCE Technical document). The BSCE Pharmaco Atlas application was used to categorize, and rank compounds based on meta-signature correlations to all "treatment versus control" Biosets in the system \[4,804 Compounds in 53,723 Biosets from 6,852 Studies on 1 January 2021\]. The BSCE Knockdown Atlas application was used to categorize, and rank genes based on meta-signature correlations to all "gene perturbation versus control" Biosets in the system \[5,341 Genes Perturbed in 37,838 Biosets from 10,287 Studies on 1 January 2021\]. The BSCE Disease Atlas application was used to categorize, and rank disease phenotypes based on queries with i) Cxcl10 and ii) meta-signature correlations to all "disease phenotype versus normal" Biosets in the system \[5,309 Phenotypes in 68,697 Biosets from 12,929 Studies on 1 January 2021\].  

Compound scores, and separately gene knockout scores, were scaled from -100 to +100 for each meta-signature timepoint and aggregated into a matrix of correlative perturbation time vectors over the course of SARS-CoV-1 infection (Supplemental Table 3). Compounds known to be in Clinical Trials were derived from https://ghddi-ailab.github.io/Targeting2019-nCoV/clinical. Knockout and Knockdown Atlas results for the 2dpi2 dpi Meta-Signature are shown in Supplemental Table 4.  

**Correlations to Human COVID-19 single cell RNAseq and Plasma Proteomic Studies.**  

Single cell RNAseq data was obtained from (Liao et al., 2020), the Supplemental Data sections in Liao et al 2020, (Schulte-Schrepping et al., 2020), (Wilk et al., 2020), and (Lee et al., 2020). Tables from each of the articles were downloaded and divided into individual cell type specific bioset files and imported into BSCE as Curated Studies for correlations to temporal meta-signature gene clusters.  

Plasma proteomic data from symptomatic COVID-19 patients and acutely ill non-COVID-19 controls was downloaded from https://www.olink.com/application/mgh-covid-19-study (Filbin et al. 2021). 

**Interactive Portal**  

The 74 Bioset and the 5 Meta-Signature results were collaboratively explored using Illumina Connected Analytics (https://www.illumina.com/products/by-type/informatics-products/connected-analytics.html) and then developed into an interactive portal using Dash (http://conference.scipy.org/proceedings/scipy2019/shammamah_hossain.html) with the following features: i) Table View with gene search and expression profile plots, ii) Principal Component Analysis, iii) Clustering HeatMaps, iv) Pharmaco (TBD?). Export of data and some results is enabled to help investigators. Access is available at this URL http://18.222.95.219:8047 . The data and code are also available at GitHub (https://github.com/Mark-A-Taylor/Coronavirus_Portal.git/).  
    '''),
    ]),
    html.Br(),
    dcc.Link('Return to Index', href='/')
])

#   @app.callback(
#       Output('methods-display-value', 'children'),
#       Input('page-1-dropdown', 'value'))
#   def display_value(value):
#       return 'You have selected "{}"'.format(value)

