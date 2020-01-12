import glob
import os
from pathlib import Path
from datetime import datetime

import s3fs

from dask import dataframe as dd
import pandas as pd

from library.config import feature_cols

DATA = Path.home().joinpath("SWI_data", "data")

def find_latest_file_s3(path):
    """Finds the latest file in an s3 path, based off of a glob string
    passed in 'path'

    Returns:
        String path leading to the latest file in a directory
    """
    fs = s3fs.S3FileSystem()
    list_of_files = fs.glob(path)
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


def drop_non_numeric_feats(df):
    """Removes non-numeric feature columns from dataframe"""
    just_numeric = df[feature_cols]
    return just_numeric


def load_dd(path):
    ddf = dd.read_csv(path)\
            .rename(columns = {"Unnamed: 0":"index"})\
            .set_index('index')
    return ddf


def load_df(path):
    df = pd.read_csv(path, index_col=0)
    return df


def save_object(object: list, object_type: str):
    """Saves list object as csv"""
    objects = pd.concat(object)
    dt = datetime.now().strftime("%d%m%Y_%H%M%S")
    objects.to_csv(f"{DATA}MORE_STUFF_HERE_{dt}.csv")
    return


def save_objects(objects: dict):
    """Takes a dictionary containing key/value paris of object listings 
    and object_types and saves each via `save_object`
    """
    for object in objects:
        save_object(object["object"], object["object_type"])
    return