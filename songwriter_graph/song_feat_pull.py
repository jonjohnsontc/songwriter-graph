from datetime import date
import glob
import json

from dask.distributed import Client
from dask import dataframe as dd

import pandas as pd

# client = Client()


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
    count = 0

    for file in files:
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
        count += 1
        if count % 100 == 0:
            print("{} files completed".format(count))

    with open(
        "../data/interim/song_features/features_{}.json".format(
            date.today().strftime("%Y%m%d")
        ),
        "w",
    ) as f:
        json.dump(base_song_features, f)
    return


def mk_song_feats_df(song_features_json_fp):
    """
    Takes new Spotify song features .json, and transforms it to
    a csv file while also eliminating unnecessary columns, and 
    transforming other columns to numerical ones
    """
    song_features_ddf = dd.read_json(song_features_json_fp, orient="index")
    clean_song_features_ddf = song_features_ddf.drop(
        axis=1, labels=["id", "track_href", "uri", "analysis_url", "type",]
    )
    clean_song_features_df = clean_song_features_ddf.compute()
    clean_song_features_df.to_csv(
        "../data/interim/song_features/song_features_{}.csv".format(
            date.today().strftime("%Y%m%d")
        )
    )

    return


def main():
    # TODO: Create something that finds the newest song features
    get_song_feats("data/song_features")
    song_features_path = glob.glob(
        "data/interim/song_features/*"
    )  # TODO: Edit into something that finds the newest file
    rm_unnecessary_entries(song_features_path)


if __name__ == "__main__":
    main()
