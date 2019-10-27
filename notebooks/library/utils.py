import glob
import os

import s3fs

from dask import dataframe as dd
import pandas as pd

def find_latest_file_s3(path):
    """Finds the latest file in an s3 path, based off of a glob string
    passed in 'path'

    Returns:
        String path leading to the latest file in a directory
    """
    fs = s3fs.S3FileSystem()
    list_of_files =fs.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def find_latest_file(path):
    """Finds the latest file in a path, based off of a glob string passed
    in 'path'

    Returns:
        String path leading to the latest file in a directory
    """
    # glob hint https://stackoverflow.com/a/39327156
    list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def load_dd(path):
    ddf = dd.read_csv(path)\
            .rename(columns = {"Unnamed: 0":"index"})\
            .set_index('index')
    return ddf


def load_df(path):
    df = pd.read_csv(path, index_col=0)
    return df