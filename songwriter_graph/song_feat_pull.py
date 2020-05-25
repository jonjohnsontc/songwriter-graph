from datetime import date
import glob
import json

import pandas as pd
from tqdm.auto import tqdm

def song_feat_pull(song_list):
    """
    Pulls modeling features of songs and outputs them into a separate list.
    """
    master_song_list = []

    for entry in song_list:
        if isinstance(entry, dict):
            for track in entry["tracks"]:
                master_song_list.append(
                    {
                        "song_id": track["id"],
                        "song_title": track["name"],
                        "artist_id": track["artists"][0]["id"],
                        "artist_name": track["artists"][0]["name"],
                        "linked_album": track["album"]["name"],
                        "album_release_date": track["album"]["release_date"],
                        "duration_ms": track["duration_ms"],
                        "explicit": track["explicit"],
                    }
                )
    return master_song_list


def get_song_feats(fp):
    """
    Retrieves Spotify song features from .json files
    """
    base_song_features = {}
    files = glob.glob("{}/*.json".format(fp))

    for file in tqdm(files):
        with open(file, "r") as f:
            dict_of_song_feats = json.load(f)
        for entry in dict_of_song_feats:
            for i in range(len(dict_of_song_feats[entry])):
                if not dict_of_song_feats[entry][i] == None:
                    base_song_features[
                        dict_of_song_feats[entry][i]["id"]
                    ] = dict_of_song_feats[entry][i]
        # for entry in dict_of_song_feats:
        #     base_song_features[count] = ['3']

    return base_song_features
