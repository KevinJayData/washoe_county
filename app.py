from IPython import embed
import shutil
import urllib.request as request
from contextlib import closing
import zipfile
import pandas as pd
import os
import download_data


def execute():
    data = download_data.download_data_from_website()
    long_df = download_data.wide_to_long_conversion(data)

    embed()
    download_data.delete_all_files()


if __name__=="__main__":
    execute()