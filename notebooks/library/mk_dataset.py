import os

import dask
from dask import dataframe as dd
from dask.distributed import Client
from dask_ml.preprocessing import DummyEncoder
import pandas as pd 
import numpy as np

from numba import jit

client = Client()

def mk_songwriter_dataset(songwriter_df, genre_song_lookup_df, pitch_timbre_df):
    '''
    Creates dataframe of songs with features ready for modeling
    '''
    if isinstance(songwriter_df, dask.dataframe.core.DataFrame)
    pass


def mk_genre_dummies(genre_song_lookup_df):
    '''
    Creates dummies out of genre to song lookup dataframe
    '''
    if os.cpu_count() is not None:
        genre_song_lookup_dd = dd.from_pandas(genre_song_lookup_df, 
                                              npartitions=os.cpu_count())
    else:
        genre_song_lookup_dd = dd.from_pandas(genre_song_lookup_df, 
                                              npartitions=16)
    de = DummyEncoder()
    genre_dummies_dd = de.fit_transform(genre_song_lookup_dd)
    return genre_dummies_dd


def create_avg_sngwrtr_value(ddf):
    '''
    Creates an average song value for each songwriter included in the 
    dataset, and is combined with the original dataset to return a 
    new dask dataframe with said avg values
    '''
    grouped_vals_ddf = ddf.groupby('WID').mean()
    ddf_with_avgs = dd.concat([
        ddf,
        grouped_vals_ddf
    ])
    return ddf_with_avgs



def mk_msong_list(song_list):
    '''
    Retrieve `track_name` and `track_id` for each song and add to separate listing.
    '''
    master_song_list = []

    for entry in song_list:
        if isinstance(entry, dict):
            for track in entry['tracks']:
                master_song_list.append(dict({track['name'] : track['id']}))
    return master_song_list