import os
import pickle as pkl

import numpy as np 
import pandas as pd 
import dask.dataframe as dd
from dask.distributed import Client
from dask_ml.wrappers import Incremental
import s3fs

import joblib
from sklearn.neighbors import NearestNeighbors

from library.config import modeling_labels_path, modeling_path
from library.utils import find_latest_file, load_dd



def get_euclidean(modeling_ready_ddf):
    modeling_ready_ddf = dd.read_csv(find_latest_file(modeling_path))\
                           .rename(columns = {"Unnamed: 0":"index"})\
                           .set_index('index')
    print("Fitting Model")
    nn = NearestNeighbors(n_neighbors=10, metric="euclidean").fit()
    nn.fit()
    nn_incremental = Incremental(nn)
    fit_ddf = nn_incremental.fit(modeling_ready_ddf)

    print("Retrieving Neighbors")
    distances, indices = nn.kneighbors(modeling_ready_ddf)
    
    print("Saving Neighbors to s3")
    # https://stackoverflow.com/a/44818887
    fs = s3fs.S3FileSystem(key=os.path.get('AWS_KEY'), secret=os.path.get('AWS_SECRET_KEY'))
    with fs.open('s3://swg_bucket/processed/distances/distances_{}.pkl', 'wb') as f:
        pkl.dump(distances, f)
    with fs.open('s3://swg_bucket/processed/indices/indices_{}.pkl', 'wb') as f:
        pkl.dump(indices, f)
    return "Finished"


if __name__ == "__main__":
    ddf = load_dd(find_latest_file(modeling_path))

    # NOTE: Do not need if I don't create DF
    # labels_ddf = dd.read_csv(find_latest_file(modeling_labels_path))\
    #                .rename(columns = {"Unnamed: 0":"index"})\
    #                .set_index('index')
    
    print("Fitting Model")
    nn = NearestNeighbors(n_neighbors=10, metric="euclidean").fit()
    nn.fit()
    nn_incremental = Incremental(nn)
    fit_ddf = nn_incremental.fit(modeling_ready_ddf)

    print("Retrieving Neighbors")
    distances, indices = nn.kneighbors(modeling_ready_ddf)

    #TODO: .ENV file
    print("Saving Neighbors to s3")
    # https://stackoverflow.com/a/44818887
    fs = s3fs.S3FileSystem(key=os.path.get('AWS_KEY'), secret=os.path.get('AWS_SECRET_KEY'))
    with fs.open('s3://swg_bucket/processed/distances/distances_{}.pkl', 'wb') as f:
        pkl.dump(distances, f)
    with fs.open('s3://swg_bucket/processed/indices/indices_{}.pkl', 'wb') as f:
        pkl.dump(indices, f)
    
    #NOTE: Toss in separate function
    # print("Building Labeled DataFrames for Neighbor Indices and Distances")
    # ds = distances.shape[0]
    # df_distances = pd.DataFrame(np.vstack(np.split(distances, ds)))
    # df_indices = pd.DataFrame(np.vstack(np.split(indices, ds)))
    # labeled_distances = pd.concat([labels_ddf,
    #                                df_distances])
    # labeled_indices = pd.concat([labels_ddf,
    #                              df_indices])

    # print("Saving Files")
    # df_indices_in_bytes = labeled_indices.to_csv(None).encode()
    # with fs.open('s3://swg_bucket/processed/indices/indices_df_{}.csv', 'wb') as f:
    #     f.write(indices)
    # df_distances_in_bytes = labeled_distances.to_csv(None).encode()
    # with fs.open('s3://swg_bucket/processed/distances/distances_df_{}.csv', 'wb') as f:
    #     f.write(distances)
    return "Finished"