import shutil
import urllib.request as request
from contextlib import closing
import zipfile
import pandas as pd
import numpy as np
import os
import warnings
import cpi
from IPython import embed


def download_data_from_website():
    """
    Download data from website
    :return: pandas dataframe of all the data
    """
    print('Downloading Data from https://www.washoecounty.us/assessor/online_data/DataDownloads.php')
    with closing(request.urlopen('ftp://GenericFiles:endjob@wcftp.washoecounty.us/GNRC/GSA_QuickInfo.zip')) as r:
        with open('data', 'wb') as f:
            shutil.copyfileobj(r, f)
    with zipfile.ZipFile('data', 'r') as zip_ref:
        zip_ref.extractall('unzip')

    chunks = pd.read_csv('unzip/Quick_Info.txt', sep="\t", chunksize=100000)
    df = pd.concat(chunks, ignore_index=True)
    return df


def wide_to_long_conversion(df):
    """
    Takes wide data of last 6 sales/owners and converts it to something manageable for analysis
    :param debug: saves me time by grabbing the file if it exits instead of getting a new one
    :param df: wide data as downloaded from the website
    :return: long df for analysis
    """
    print('Melting the df')
    samt = ['SAMT1', 'SAMT2', 'SAMT3', 'SAMT4', 'SAMT5', 'SAMT6']
    sdat = ['SDAT1', 'SDAT2', 'SDAT3', 'SDAT4', 'SDAT5', 'SDAT6']
    scod = ['SCOD1', 'SCOD2', 'SCOD3', 'SCOD4', 'SCOD5', 'SCOD6']
    luc = ['LUCatSAle1', 'LUCatSAle2', 'LUCatSAle3', 'LUCatSAle4', 'LUCatSAle5', 'LUCatSAle6']
    grantor = ['GrantorLastName1', 'GrantorLastName2', 'GrantorLastName3', 'GrantorLastName4', 'GrantorLastName5',
               'GrantorLastName6']

    value_vars = [samt, sdat, scod, luc, grantor]
    flat_vars = [item for sublist in value_vars for item in sublist]
    wanted_columns = [item for item in list(df.columns) if item not in flat_vars]
    df.drop_duplicates(subset='ParcelID', inplace=True)

    long_dict = {}
    for i in range(len(value_vars)):
        print('Elongating var: ' + str(value_vars[i][0][:-1]))
        long_dict[str(value_vars[i][0][:-1])] = df.melt(id_vars=df[wanted_columns], value_vars=value_vars[i],
                                                        var_name=str(value_vars[i][0][:-1]),
                                                        value_name=str(value_vars[i][0][:-1]) + '_value')

    long_df = pd.concat([long_dict['SAMT'],
                         long_dict['SDAT'][long_dict['SDAT'].columns[-2:]],
                         long_dict['SCOD'][long_dict['SCOD'].columns[-2:]],
                         long_dict['LUCatSAle'][long_dict['LUCatSAle'].columns[-2:]],
                         long_dict['GrantorLastName'][long_dict['GrantorLastName'].columns[-2:]],
                         ], axis=1)

    return long_df


def inflation_adjust(long_df):
    long_df['cpi_year'] = long_df['SDAT_value'].str.strip()
    long_df.drop(long_df[long_df.cpi_year == ''].index, inplace=True)

    long_df['cpi_year'] = pd.to_datetime(long_df['cpi_year']).dt.to_period('Y')
    long_df['cpi_year'] = long_df.cpi_year.astype(str).astype(int)
    long_df.drop(long_df[long_df.cpi_year < 1950].index, inplace=True)
    long_df.reset_index(drop=True, inplace=True)

    long_df['cpi_samt_value'] = long_df.apply(lambda x: x.SAMT_value*0.97 if x.cpi_year in (2019, 2020) else cpi.inflate(x.SAMT_value, x.cpi_year, to=2018), axis=1)
    long_df['cpi_samt_value_log'] = np.log(long_df['cpi_samt_value'])

    print('There are {} property sales in our dataset'.format(len(long_df)))
    return long_df


def delete_all_files(debug):
    if not debug:
        if os.path.exists('unzip'):
            shutil.rmtree('unzip')
        if os.path.exists('data'):
            os.remove('data')
        if os.path.exists('long_df.csv'):
            os.remove('long_df.csv')
        print('All files deleted, thanks for enjoying my project')