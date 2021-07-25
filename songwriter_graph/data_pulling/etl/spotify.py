"""Functions for pulling apart data structures encountered in the Spotify
API
"""
import sys

import pandas as pd


# I've currently decided that I don't care about keeping 
# category id's tied to playlists
def get_playlists_from_category_playlist(category_playlists: dict) -> list:
    categories = list(category_playlists.keys())
    playlists = []

    for category in categories:
        for playlist in category_playlists[category]["playlists"]["items"]:
            playlists.append(
                {
                    "playlist_id": playlist.get("id"),
                    "playlist_name": playlist.get("name"),
                    "snapshot_id": playlist.get("snapshot_id"),
                    "uri": playlist.get("uri")
                }
            )        
        
    return playlists

# Test script for pulling playlists out of category playlist listings
if __name__ == "__main__":
    cat_playlists = pd.read_json(sys.argv[1])
    cat_playlists_as_dict = cat_playlists.to_dict()
    playlists = get_playlists_from_category_playlist(cat_playlists_as_dict)
