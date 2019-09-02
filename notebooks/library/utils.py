import glob
import os

from dask import dataframe as dd

def find_latest_file(path):
    """Finds the latest file in a path, based off of a glob string passed
    in 'path'
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