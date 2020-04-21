import shutil
import urllib.request as request
from contextlib import closing
import zipfile
import pandas as pd
import os
import download_data
import analysis.graph as graph


def execute(debug=False):
    if debug and os.path.exists('long_df.csv'):
        print('Using Data we already have on hand')
        chunks = pd.read_csv('long_df.csv', sep=',', chunksize=200000)
        long_df = pd.concat(chunks, ignore_index=True)
    else:
        print('Grabbing new data')
        # Grab and clean data
        data = download_data.download_data_from_website()
        long_df = download_data.wide_to_long_conversion(data)
        long_df = download_data.inflation_adjust(long_df)
        if debug:
            print('debug is on, saving data for later')
            long_df.to_csv('long_df.csv', sep=',')

    # Begin exploratory analysis of the data

    graph.histograms(long_df)
    graph.median_housing_price_per_year(long_df)




    download_data.delete_all_files(debug)


if __name__=="__main__":
    execute()
