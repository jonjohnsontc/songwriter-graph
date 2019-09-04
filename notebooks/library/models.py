import argparse
from datetime import datetime
import os
import pickle as pkl

import numpy as np 
import pandas as pd 
import dask.dataframe as dd
from dask.distributed import Client
import s3fs

import joblib
from sklearn.neighbors import NearestNeighbors

from library.config import modeling_labels_path, modeling_path
from library.utils import find_latest_file, find_latest_file_s3, load_dd, load_df

TIME_AT_RUN = datetime.utcnow()


def get_euclidean(modeling_ready_ddf):
    print("Fitting Model")

    #TODO: Look at joblib for potential parallelism across operations
    #https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html#joblib.Parallel
    nn = NearestNeighbors(n_neighbors=10, metric="euclidean", n_jobs=-1)
   
    #NOTE: Formerly used "Incremental", but `n_jobs` controls parallelism
    nn.fit(modeling_ready_ddf)

    print("Retrieving Neighbors")
    distances, indices = nn.kneighbors(modeling_ready_ddf)
    
    print("Saving Neighbors to s3")
    # https://stackoverflow.com/a/44818887
    fs = s3fs.S3FileSystem()
    with fs.open(f's3://swg_bucket/processed/distances/distances_{TIME_AT_RUN}.pkl', 'wb') as f:
        pkl.dump(distances, f)
    with fs.open(f's3://swg_bucket/processed/indices/indices_{TIME_AT_RUN}.pkl', 'wb') as f:
        pkl.dump(indices, f)
    
    print("Finished")
    return distances, indices


def create_model_df(labels, matrix, type_of_file):
    """Takes in song labels, along with distances and indices of neighbors
    to produce a more easily interpretable dataset

    Args:
        labels: Pandas DataFrame, a dataframe of label values
        matrix: Numpy ndarray of either distances or indices computed
                from some NearestNeighbors modeling method
        type_of_file: str, either "distances" or "indices" for now,
                      although this could change with other models
                      being constructed.

    Returns:
        "Finished" Message, after saving 
    """
    ms = matrix.shape[0]
    df_matrix = pd.DataFrame(np.vstack(np.split(matrix, ms)))
    labeled_matrix = pd.concat([labels,df_matrix])

    print("Saving Files")
    df_matrix_in_bytes = labeled_matrix.to_csv(None).encode()
    fs = s3fs.S3FileSystem()
    with fs.open(f's3://swg_bucket/processed/{type_of_file}/{type_of_file}_df_{TIME_AT_RUN}.csv', 'wb') as f:
        f.write(df_matrix_in_bytes)
    return "Finished"

def parse_args():
    parser = argparse.ArgumentParser('Description: Generate models based on songwriter data passed through')
    parser.add_argument(
        "path",
        help="Location of the modeling ready songwriter data",
        type=str)
    return vars(parser.parse_args())



if __name__ == "__main__":
    args = parse_args()
    ddf = load_dd(find_latest_file_s3(args['path']))
    dist, indices = get_euclidean(ddf)
