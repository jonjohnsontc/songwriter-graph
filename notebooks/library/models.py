import numpy as np 
import pandas as pd 

import dask.dataframe as dd
from dask.distributed import Client
from dask_ml.wrappers import Incremental


def get_jaccard():
    pass


if __name__ == "__main__":
    modeling_ready_ddf = dd.read_csv("../data/modeling/scaled_ddf_20190825.csv")\
                           .rename(columns = {"Unnamed: 0":"index"})\
                           .set_index('index')
    labels_ddf = dd.read_csv("../data/modeling/metadata_for_scaled_ddf_2019825")\
                   .rename(columns = {"Unnamed: 0":"index"})\
                   .set_index('index')
    
    

    df_indices.to_csv("")
    df_distances.to_csv("")
    return "Finished"