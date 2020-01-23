import glob
import os
from pathlib import Path, PurePath
from datetime import datetime
import json

import s3fs

import dask
import dask.dataframe as dd
import pandas as pd
import numpy as np

from songwriter_graph.config import feature_cols

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

@dask.delayed
def load_json(path: PurePath) -> dict:
    with path.open() as f:
        obj = json.load(f)
    return obj


def get_files(path: str) -> list:
    filepaths = DATA.joinpath(path).glob("*.json")
    return filepaths

# More precise types here
def save_object(object_list: list, object_type: str):
    """Saves list object as csv"""
    object_map = {
        "sec_mean_vars": Path("interim", "sections", "means_vars"),
        "pt_mean_vars": Path("interim", "pitch_timbre", "means_vars"),
        "pt_pcas": Path("interim", "pitch_timbre", "pca"),
        "key_changes": Path("interim", "sections", "key_changes")
    }
    objects = pd.concat(object_list)
    dt = datetime.now().strftime("%d%m%Y_%H%M%S")
    path = DATA.joinpath(object_map[object_type])
    objects.to_csv(path.joinpath(f"{object_type}_{dt}.csv"))
    return


def save_objects(objects: list):
    """Takes a dictionary containing key/value paris of object listings 
    and object_types and saves each via `save_object`
    """
    for item in objects:
        save_object(item["object"], item["object_type"])
    return


def save_object_np(
    object_list: list, 
    object_type: str, 
    schema: list, 
    song_ids: list):
    """Saves list object as csv"""
    object_map = {
        "sec_mean_vars": Path("interim", "sections", "means_vars"),
        "pt_mean_vars": Path("interim", "pitch_timbre", "means_vars"),
        "pt_pcas": Path("interim", "pitch_timbre", "pca"),
        "key_changes": Path("interim", "sections", "key_changes")
    }
    objects = _create_df(object_list, schema, song_ids)
    dt = datetime.now().strftime("%d%m%Y_%H%M%S")
    path = DATA.joinpath(object_map[object_type])
    objects.to_csv(path.joinpath(f"{object_type}_{dt}.csv"))
    return


def save_objects_np(objects: list):
    for item in objects:
        save_object_np(item["object"], item["object_type"], item["columns"], item['object_index'])
    return

def _create_df(array: np.ndarray, columns: list, song_ids: list) -> pd.core.frame.DataFrame:
    return pd.DataFrame(array, columns=columns, index=song_ids)