from IPython import embed
import shutil
import urllib.request as request
from contextlib import closing
import zipfile
import pandas as pd
import os


def execute():

    # Download data from website
    if not os.path.exists('unzip/Quick_Info.txt'):
        with closing(request.urlopen('ftp://GenericFiles:endjob@wcftp.washoecounty.us/GNRC/GSA_QuickInfo.zip')) as r:
            with open('data', 'wb') as f:
                shutil.copyfileobj(r, f)
        with zipfile.ZipFile('data', 'r') as zip_ref:
            zip_ref.extractall('unzip')

    # If it exists already just read it in
    df = pd.read_csv('unzip/Quick_Info.txt', sep="\t")


    embed()


if __name__=="__main__":
    execute()