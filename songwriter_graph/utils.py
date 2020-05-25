import glob
import os
from pathlib import Path, PurePath
from datetime import datetime
import json
from typing import Generator, Union

import s3fs
import os
import pandas as pd
import numpy as np

from sqlalchemy.engine import create_engine
from psycopg2.extensions import connection
# from dotenv import load_dotenv
# load_dotenv()

from songwriter_graph.config import feature_cols

DATA = Path.home().joinpath("dev", "swg", "SWI_data", "data")

# def connect_to_postgres() -> connection:
#     # postgresql+psycopg2://user:password@host:port/dbname
#     conn = create_engine(
#         f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/postgres"
#     )
#     return conn


def find_latest_file_s3(path: Union[str,Path]):
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


def load_df(path):
    df = pd.read_csv(path, index_col=0)
    return df


def get_files(path: str) -> Generator:
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


def save_object_sql(
    object_list: list,
    object_type: str,
    columns: list,
    song_ids: list
    ):
    """Saves list object to SQLite"""
    object_map = {
        "sec_mean_vars": Path("interim", "sections", "means_vars"),
        "pt_mean_vars": Path("interim", "pitch_timbre", "means_vars"),
        "pt_pcas": Path("interim", "pitch_timbre", "pca"),
        "key_changes": Path("interim", "sections", "key_changes")
    }
    objects = pd.DataFrame(data=object_list, columns=columns)
    objects = pd.concat([song_ids,objects])
    dt = datetime.now().strftime("%%m%Y_%H%M%S")
    path = DATA.joinpath(object_map[object_type])
    # objects.to_csv(path.joinpath(f"{object_type}_{dt}.csv"))
    objects.to_sql()
    
def save_object_np(
    object_list: list, 
    object_type: str, 
    columns: list, 
    song_ids: list):
    """Saves list object as csv"""
    object_map = {
        "sec_mean_vars": Path("interim", "sections", "means_vars"),
        "pt_mean_vars": Path("interim", "pitch_timbre", "means_vars"),
        "pt_pcas": Path("interim", "pitch_timbre", "pca"),
        "key_changes": Path("interim", "sections", "key_changes")
    }
    objects = pd.DataFrame(
        data=object_list, 
        columns=columns, 
        )
    song_ids_series = pd.Series(song_ids)
    objects = pd.concat([song_ids_series,objects], axis=1)
    dt = datetime.now().strftime("%d%m%Y_%H%M%S")
    path = DATA.joinpath(object_map[object_type])
    objects.to_csv(path.joinpath(f"{object_type}_{dt}.csv"))
    return

def save_objects_np(objects: list):
    for item in objects:
        save_object_np(item["object"], item["object_type"], item["columns"], item['object_index'])
    return
