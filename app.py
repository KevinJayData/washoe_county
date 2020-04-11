from IPython import embed
import shutil
import urllib.request as request
from contextlib import closing
import zipfile
import pandas as pd
import os
import download_data


def execute(debug=False):
    data = download_data.download_data_from_website(debug)
    long_df = download_data.wide_to_long_conversion(debug, data)

    # embed()
    download_data.delete_all_files(debug)


if __name__=="__main__":
    execute()