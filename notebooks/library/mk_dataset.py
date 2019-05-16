import glob
import os

import dask
from dask import dataframe as dd
from dask.distributed import Client
from dask_ml.preprocessing import DummyEncoder
import pandas as pd 
import numpy as np

from numba import jit


# client = Client('scheduler:8786')
def _find_latest_file(path):
    '''
    Finds the latest file in a path, based off of a glob string passed
    in 'path'
    '''
    # glob hint https://stackoverflow.com/a/39327156
    list_of_files = glob.glob(path)
    latest_file = max(list_of_files)
    return latest_file
    

def mk_songwriter_dataset(songwriter_df_path, 
                        genre_song_lookup_df_path, 
                        pitch_timbre_df_path, 
                        song_features_path):
    '''
    Creates dataframe of songs with features ready for modeling
    '''
    list_of_paths = [
        songwriter_df_path,
        genre_song_lookup_df_path,
        pitch_timbre_df_path,
        song_features_path,
    ]
    latest_file_list = list(map(_find_latest_file, list_of_paths))

    songwriter_df = dd.read_csv(latest_file_list[0])
    genre_song_lookup_df = dd.read_csv(latest_file_list[1])
    pitch_timbre_df = dd.read_csv(latest_file_list[2])
    song_features_df = dd.read_csv(latest_file_list[3])

    songwriter_and_genres = dd.merge(songwriter_df, 
                                genre_song_lookup_df,
                                on = 'song_id' )
    songwriter_genres_and_pt = dd.merge(songwriter_and_genres,
                                        pitch_timbre_df,
                                        on = 'track_id')
    ready_for_modeling_df = dd.merge(songwriter_genres_and_pt,
                                        song_features_df,
                                        on = 'track_id')
    return ready_for_modeling_df



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
    return grouped_vals_ddf


def normalize_sngwriter(ddf):
    grouped_vals_ddf = ddf.groupby('WID').apply(lambda x: x / x.mean() )
    return grouped_vals_ddf


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