import inspect

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import math

from app import app, cache

# TODO: allow some 'memory' of user manipulations using stored share data by
# leveraging strategy for 'User-Based Session Data on the Server' discussed here:
#  https://dash.plotly.com/sharing-data-between-callbacks

#@cache.memoize()
def fixed_params():
    fname = inspect.stack()[0][3]
    # print("In: ",fname)
    param_dict = {
        'VERBOSITY' : 0, #1,
        'NUM_SIG_DIGITS' : 2,  # digits after the decimal for means and stdevs
        'DPI_COL' : 'Day Post-Infection',
        'DPI_VALS' : [
            0.5
            , 1
            , 2
            , 4
            , 7],
        'KEY_COLS' : [
            'GEO ID, link'
            , 'Day Post-Infection'
            , 'SARS-CoV Strain'
            , 'Host Age Cat'
            , 'Viral Dose'],
        # HACK - ASSUMES order of genes and continuity w/r/t side-by-side columns
        'GENE_COL_START' : 'March1',
        'GENE_COL_END' : 'Zzz3',
        'BIOSET_COL_START' : 'Day Post-Infection',
        'BIOSET_COL_END' : 'Lab',
        'BIOSET_COLS': [
            'GEO ID, link',
            'Day Post-Infection',
            'SARS-CoV Strain',
            'Viral Dose',
            'Host Age Category',
            'Species',
            'Article PubMed ID',
            'Viral Strain',
            'Sample Source (strain, cell)',
            'Host Mouse Strain',
            'Sex',
            'Test Samples',
            'Control Samples',
            'Feature Size',
            'Host Age',
            'Bioset name',
            'Study name',
            'Technology',
            'Lab',
            #'Bioset ID of SARS CoV-Round3BV2_74 Biosets_wZero Time Point.jmp'
            #'Viral Dose (PFUs)',
            #'Viral Severity',
            # 'Host Age Cat',
            ]
    }
    return param_dict

#########################################################
#  Data wrangling routines
def append_meta_data_keys(df,param_dict):
    # TODO? dynamic input of keys of arbitrary length and type (low priority)
    #   upside: then it would be more portable to other data sets
    # NOTE: Uses global variable KEY_COLS
    fname = inspect.stack()[0][3]
    check_col = 'Count'
    KEY_COLS = param_dict['KEY_COLS']
    VERBOSITY = param_dict['VERBOSITY']
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
            for index,row in df.iterrows():
                print('DEBUG: ',fname,': ', row['my_key'])
    # all good!
    return True

@cache.memoize()
def extract_genexp_features(df, param_dict):
    fname = inspect.stack()[0][3]
    GENE_COL_START = param_dict['GENE_COL_START']
    GENE_COL_END = param_dict['GENE_COL_END']
    VERBOSITY = param_dict['VERBOSITY']
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
        print('ERROR: ',fname, ': No gene features found.')
    return gene_features

#def extract_bioset_chars(df, param_dict):
#    fname = inspect.stack()[0][3]
#    BIOSET_COL_START = param_dict['BIOSET_COL_START']
#    BIOSET_COL_END = param_dict['BIOSET_COL_END']
#    VERBOSITY = param_dict['VERBOSITY']
#    icol_start = df.columns.get_loc(BIOSET_COL_START)
#    icol_end = df.columns.get_loc(BIOSET_COL_END)
#    if VERBOSITY > 0:
#        print('DEBUG: ',fname, ': BIOSET_COL_START: ',BIOSET_COL_START, ', icol_start: ',icol_start)
#        print('DEBUG: ',fname, ': BIOSET_COL_END: ',BIOSET_COL_END, ', icol_end: ',icol_end)
#    bioset_chars = df.iloc[:, icol_start:icol_end + 1]
#    if VERBOSITY > 0:
#        print('DEBUG: ',fname, ': shape bioset_chars: ', bioset_chars.shape)
#    if bioset_chars.shape[0] < 1:
#        print('ERROR: ',fname, ': No bioset_chars data found.')
#    return bioset_chars

#@cache.memoize()
def extract_bioset_chars(df, param_dict):
    fname = inspect.stack()[0][3]
    keeper_cols = param_dict['BIOSET_COLS']
    VERBOSITY = param_dict['VERBOSITY']
    if VERBOSITY > 0:
        print('DEBUG: ',fname, ': BIOSET_COLS: ',keeper_cols)
    bioset_chars = df[keeper_cols]
    if VERBOSITY > 0:
        print('DEBUG: ',fname, ': shape bioset_chars: ', bioset_chars.shape)
        print('DEBUG: ',fname, ': columns bioset_chars: ', bioset_chars.columns)
    if bioset_chars.shape[0] < 1:
        print('ERROR: ',fname, ': No bioset_chars data found.')
    return bioset_chars






def build_gene_time_series(df, param_dict):
    # strategy: pull list of gene and DPI and populate matrix
    # output matrix will have one row for each gene with a mean and sdev pair for each DPI
    fname = inspect.stack()[0][3]
    NUM_SIG_DIGITS = param_dict['NUM_SIG_DIGITS']
    DPI_VALS = param_dict['DPI_VALS']
    DPI_COL = param_dict['DPI_COL']
    VERBOSITY = param_dict['VERBOSITY']
    fname = inspect.stack()[0][3]
    gene_features = extract_genexp_features(df, param_dict)
    if gene_features.shape[0] < 1:
        print('ERROR: ', fname, ': Exiting.')
        exit()
    gene_ts_mean = pd.DataFrame()  # results target
    gene_ts_std = pd.DataFrame()  # results target
    for dpi_val in DPI_VALS:
        if VERBOSITY > 0:
            print('DEBUG: ', fname, ': dpi_val:', dpi_val)
        data_set = gene_features[df[DPI_COL] == dpi_val]
        #col_name = 'Mean('+str(dpi_val)+')'
        col_name = str(dpi_val)+' DPI'
        gene_ts_mean[col_name] =  round(data_set.mean(),NUM_SIG_DIGITS)
        col_name = 'Std('+str(dpi_val)+')'
        gene_ts_std[col_name] =  round(data_set.std(),NUM_SIG_DIGITS)
    gene_ts_mean.index.name = 'Gene'
    gene_ts_mean.reset_index(inplace=True)
    gene_ts_std.index.name = 'Gene'
    gene_ts_std.reset_index(inplace=True)
    return [gene_ts_mean, gene_ts_std]

def calc_feature_means(mat, nrows, ncols, debug=False):
    #means = [];
    if debug:
        print("calc_feature_means: nrows, ncols, mat: ",nrows, ncols, mat)
    # Calculate sums
    #for jjj in range(ncols):
    #    column_sum = 0.
    #    for iii in range(nrows):
    #        if debug:
    #            print("mat iii,jjj: ",iii,jjj,mat[iii][jjj])
    #        column_sum += mat[iii][jjj]
    #    means.append(column_sum/nrows)
    means = mat.mean(0)
    # Return mean
    return means


def calc_feature_vars(mat, nrows, ncols, debugBool=False, centerBool=True):
    varz = []
    if debugBool:
        print("calc_feature_vars: nrows, ncols, mat: ",nrows, ncols, mat)
    #
    if centerBool:
        varz = np.var(mat,axis=0,ddof=1)
    else:
        # using blue collar way to compute the variance 
        # asot numpy.var() so we can support 'noncentered' calcs
        if isinstance(mat,pd.DataFrame):
            mat2 = mat.to_numpy()
        else:
            mat2 = mat
        for jjj in range(ncols):
            column_sum = 0.
            for iii in range(nrows):
                # subtract mean and square each term
                contrib = mat2[iii][jjj]
                contrib *= contrib
                column_sum += contrib
            # NOTE: sample variance (N-1) asot population (N)
            varz.append(column_sum/(nrows-1))
    return varz


@cache.memoize()
def calc_data(params):
    # routine to map the single input data file into
    # some calculated results stored in cache to speed up
    # loading/debugging
    #
    fname = inspect.stack()[0][3]
    input_file_folder = './data/'
    input_file_name = "SARS_CoV_Round4v2_74_Biosets_wZero_Time_Point.txt"
    filepath_name = input_file_folder + input_file_name
    seventyfour = pd.read_csv(filepath_name, sep='\t', lineterminator='\n')

    # we also want a version of the data without the rows for graphing the zero time point
    seventyfour_nozeros = (seventyfour.head(74)).copy(deep=True)

    # add a column 'Count' to allow us to pivot data and get sums for meta data characteristics
    seventyfour_nozeros['Count'] = 1

    # build/append a unique key for each meta sample for MDA
    # These keys are used for hover data
    if not append_meta_data_keys(seventyfour_nozeros, params):
        print('ERROR: ',fname,': Exiting.' )
        exit(1)

    # compute time series means & sdevs across meta samples for each gene
    [gene_ts_mean, gene_ts_std] = build_gene_time_series(seventyfour_nozeros, params)
    if gene_ts_mean.shape[0] < 1 or gene_ts_std.shape[0] < 1:
        print('ERROR: ', fname, ': Exiting.')
        exit(2)
    #
    bioset_chars = extract_bioset_chars(seventyfour_nozeros, params)
    if bioset_chars.shape[0] < 1 or bioset_chars.shape[0] < 1:
        print('ERROR: ', fname, ': Exiting.')
        exit(3)
    #
    return [ seventyfour, seventyfour_nozeros, gene_ts_mean, gene_ts_std, bioset_chars]

@cache.memoize()
def calc_pcas(params, data, nsample, nfeature, normalization='Center', ncomps=3):
    # routine to calculate PCAs for data
    #   rows are samples
    #   columns are features
    #
    # normalization options:
    #    'None' => use the data samples raw
    #    'Center' => standard PCA analysis - center the features to each have mean=zero
    #    'Normalize' => scale each sample row to a unit vector - NOT SUPPORTED
    #    'Standardize' => scale each feature column to unit variance
    #
    # traditional PCA and then projected onto first 3 components - CENTERED
    fname = inspect.stack()[0][3]
    VERBOSITY = params['VERBOSITY']
    rc = 0
    if nsample < 1:
        print('ERROR: ', fname, ': ERROR - bad nsample input.')
        return(-1,None,None,0,None)
    elif nfeature < 1:
        print('ERROR: ', fname, ': ERROR - bad nfeature input.')
        return(-2,None,None,0,None)
    elif data.shape[0] < 1:
        print('ERROR: ', fname, ': ERROR - no data rows.')
        return(-1,None,None,0,None)
    elif data.shape[1] < 1:
        print('ERROR: ', fname, ': ERROR - no feature columns.')
        return(-2,None,None,0,None)

    # optional output of some basic properties of the data
    if VERBOSITY:
        # manually calc some variance results:
        feature_means = calc_feature_means(data,nsample,nfeature)
        print(fname,": matrix data shape: ",data.shape)
        print(fname,": matrix feature means: ",feature_means)
        feature_origin_varz = calc_feature_vars(data,nsample,nfeature,centerBool=False)
        var_origin_sum = np.sum(feature_origin_varz)
        print(fname,": matrix NONCENTERED variance (relative to origin): {:.5f}".format(var_origin_sum))
        for iii in range(nfeature):
            print("  Feature",iii+1,": var {:.5f}".format(feature_origin_varz[iii]),
                "( {:.2f} %)".format(100*feature_origin_varz[iii]/var_origin_sum))
        feature_varz = calc_feature_vars(data,nsample,nfeature,centerBool=True)
        var_sum = np.sum(feature_varz)
        print(fname,": matrix CENTERED variance: {:.5f} (relative to feature means)".format(var_sum))
        for iii in range(nfeature):
            print("  Feature",iii+1,": var {:.5f}".format(feature_varz[iii]),
                "( {:.2f} %)".format(100*feature_varz[iii]/var_sum))

    if (normalization == 'Center'):
        pcas = PCA(n_components=ncomps)
        pcas.fit(data)
        projection = pcas.transform(data)
        if VERBOSITY > 0:
            print(fname,": CENTERED using sklearn PCA():")
            print("  total variance explained: {:.5f}".format(np.sum(pcas.explained_variance_)))
            cum_frac = 0.
            cum_var = 0.
            for iii in range(0,ncomps):
                val_var = pcas.explained_variance_[iii]
                val_frac = pcas.explained_variance_ratio_[iii]
                cum_var += val_var
                cum_frac += val_frac
                print("  PC",iii+1,": var {:.5f}".format(val_var),
                    "( {:.2f} %)".format(100*val_frac),
                    ", cum var: {:.5f}".format(cum_var),
                    "({:.2f} %)".format(100*cum_frac))
            print("  PC projection: ")
            print("  ",projection)
        explained_variance = pcas.explained_variance_
        explained_variance_ratio = pcas.explained_variance_ratio_
        pca_total_var = np.sum(pcas.explained_variance_)

        ########################################################
        ## Alternative calcs using numpy SVD 
        ## SVD values 
        #feature_means = calc_feature_means(data,nsample,nfeature)
        #eee = data - feature_means
        #uuu,sigma,vvvT = np.linalg.svd(eee,full_matrices=False)
        #sss = np.diag(sigma)
        #total_svd_var = np.dot(sigma,sigma.T)/(nsample-1)
        #if VERBOSITY:
        #    print(fname,": CENTERED using numpy SVD():")
        #    print("  SVD total variance (relative to feature means): {:.5f}".format(total_svd_var))
        #    cum_frac = 0.
        #    cum_var = 0.
        #    for iii in range(0,ncomps): 
        #        val_var = sigma[iii]*sigma[iii]/(nsample-1)
        #        val_frac = val_var/total_svd_var
        #        cum_frac += val_frac
        #        cum_var += val_var
        #        print("  SVD: ",iii+1,", singular value: {:.5f}".format(sigma[iii]),
        #              ", var: {:.5f}".format(val_var),
        #              "({:.2f} %)".format(100*val_frac),
        #              ", cum var: {:.5f}".format(cum_var),
        #              "({:.2f} %)".format(100*cum_frac))
        #    reconstruct_data = np.dot( uuu[ : , :ncomps], np.dot( sss[ :ncomps, :ncomps ], vvvT[ :ncomps, : ] ) )
        #    projection2 = np.dot( uuu[ : , :ncomps], sss[ :ncomps, :ncomps ])
        #    check_var = calc_feature_vars(reconstruct_data,nsample,nfeature,centerBool=True)
        #    check_var_sum = np.sum(check_var)
        #    print("  SVD variance check on reconstruction: {:.5f} (relative to feature means)".format(check_var_sum))
        #    print("  SVD projection:")
        #    print("  ",projection2)
        ########################################################

    elif (normalization == 'Standardize'):
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        pcas = PCA(n_components=ncomps)
        pcas.fit(scaled_data)
        projection = pcas.transform(scaled_data)
        if VERBOSITY > 0:
            print(fname,": STANDARDIZE using sklearn PCA():")
            print("  total variance explained: {:.5f}".format(np.sum(pcas.explained_variance_)))
            cum_frac = 0.
            cum_var = 0.
            for iii in range(0,ncomps):
                val_var = pcas.explained_variance_[iii]
                val_frac = pcas.explained_variance_ratio_[iii]
                cum_var += val_var
                cum_frac += val_frac
                print("  PC",iii+1,": var {:.5f}".format(val_var),
                    "( {:.2f} %)".format(100*val_frac),
                    ", cum var: {:.5f}".format(cum_var),
                    "({:.2f} %)".format(100*cum_frac))
            print("  PC projection: ")
            print("  ",projection)
        explained_variance = pcas.explained_variance_
        explained_variance_ratio = pcas.explained_variance_ratio_
        pca_total_var = np.sum(pcas.explained_variance_)

        ########################################################
        ## Alternative calcs using numpy SVD w StandardScalar()
        ## SVD values 
        #print(fname,": STANDARDIZE using numpy SVD:")
        #feature_means = calc_feature_means(scaled_data,nsample,nfeature)
        #uuu,sigma,vvvT = np.linalg.svd(scaled_data,full_matrices=False)
        #sss = np.diag(sigma)
        #total_svd_var = np.dot(sigma,sigma.T)/(nsample-1)
        #print("  SVD total variance (relative to feature means): {:.5f}".format(total_svd_var))
        #cum_frac = 0.
        #cum_var = 0.
        #for iii in range(0,ncomps): 
        #    val_var = sigma[iii]*sigma[iii]/(nsample-1)
        #    val_frac = val_var/total_svd_var
        #    cum_frac += val_frac
        #    cum_var += val_var
        #    print("  SVD: ",iii+1,", singular value: {:.5f}".format(sigma[iii]),
        #          ", var: {:.5f}".format(val_var),
        #          "({:.2f} %)".format(100*val_frac),
        #          ", cum var: {:.5f}".format(cum_var),
        #          "({:.2f} %)".format(100*cum_frac))
        #reconstruct_data = np.dot( uuu[ : , :ncomps], np.dot( sss[ :ncomps, :ncomps ], vvvT[ :ncomps, : ] ) )
        #projection2 = np.dot( uuu[ : , :ncomps], sss[ :ncomps, :ncomps ])
        #check_var = calc_feature_vars(reconstruct_data,nsample,nfeature,centerBool=True)
        #check_var_sum = np.sum(check_var)
        #print("  SVD variance check on reconstruction: {:.5f} (relative to feature means)".format(check_var_sum))
        #print("  SVD projection:")
        #print("  ",projection2)
        ########################################################

    elif (normalization == 'None'):
        # SVD on the raw data
        uuu,sigma,vvvT = np.linalg.svd(data,full_matrices=False)
        sss = np.diag(sigma)
        # HACK: flip the direction of the first vector so projection is more intuitive
        # TODO: implement 'SignFlip' function from : https://www.osti.gov/servlets/purl/920802
        uuu[ : , 0] = -1.*uuu[ : , 0]
        vvvT[ 0 , : ] = -1.*vvvT[ 0 , : ]
        if VERBOSITY > 0:
            print("uuu:")
            print(uuu)
            print("sss:")
            print(sss)
            print("vvvT:")
            print(vvvT)
        projection = np.dot( uuu[ : , :ncomps], sss[ :ncomps, :ncomps ])
        total_svd_var = np.dot(sigma,sigma.T)/(nsample-1)
        if VERBOSITY > 0:
            print(fname,": NONE using numpy SVD values (NONCENTERED):")
            print("  SVD total variance (relative to feature means): {:.5f}".format(total_svd_var))
        cum_frac = 0.
        cum_var = 0.
        explained_variance = []
        explained_variance_ratio = []
        for iii in range(0,ncomps):
            val_var = sigma[iii]*sigma[iii]/(nsample-1)
            val_frac = val_var/total_svd_var
            explained_variance.append(val_var)
            explained_variance_ratio.append(val_frac)
            cum_frac += val_frac
            cum_var += val_var
            if VERBOSITY > 0:
                print("  SVD: ",iii+1,", singular value: {:.5f}".format(sigma[iii]),
                      ", var: {:.5f}".format(val_var),
                      "({:.2f} %)".format(100*val_frac),
                      ", cum var: {:.5f}".format(cum_var),
                      "({:.2f} %)".format(100*cum_frac))
        if VERBOSITY > 0:
            reconstruct_data = np.dot( uuu[ : , :ncomps], np.dot( sss[ :ncomps, :ncomps ], vvvT[ :ncomps, : ] ) )
            check_var = calc_feature_vars(reconstruct_data,nsample,nfeature,centerBool=False)
            check_var_sum = np.sum(check_var)
            print("  SVD variance check on reconstruction: {:.5f} (relative to origin)".format(check_var_sum))
            print("  input data:")
            print(data)
            print("  SVD reconstruction:")
            print(reconstruct_data)
            print("  SVD projection:")
            print(projection)
    else:
        return(-3,None,None,0,None)
    return [rc, explained_variance, explained_variance_ratio, ncomps, projection]



def split_filter_part(filter_part):
    operators = [['ge ', '>='],
                ['le ', '<='],
                ['lt ', '<'],
                ['gt ', '>'],
                ['ne ', '!='],
                ['eq ', '='],
                ['contains '],
                ['datestartswith ']]

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
                    if 'contains ' == operator:
                        # treat any numeric values with 'contains' as strings
                        value = value_part
                    else:
                        try:
                            value = float(value_part)
                        except ValueError:
                            value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value
    return [None] * 3


