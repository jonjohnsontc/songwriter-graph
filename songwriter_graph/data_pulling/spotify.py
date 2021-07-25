import json
import logging
import os
import psycopg2
import sys
import spotipy

from spotipy.exceptions import SpotifyException
from sqlalchemy.engine import create_engine
from typing import List
from dotenv import load_dotenv

# TODO: I tossed the `db` folder as a child of `data_pulling` while I work on
#       getting an idea of how I should build the data pulling from spotify
#       steps. It should probably be moved back 
from db.queries.spotify import get_category_result, get_playlists, insert_tracks

# TODO: Make sure I remove this before merging to master
load_dotenv("/Users/jonjohnson/dev/swg/Song_Index/.env")


def connect_to_postgres():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/postgres"
    )
    conn = engine.connect()
    return conn


def authorize_client() -> spotipy.Spotify:
    """Logs into the spotify api. Returns a spotipy Spotify client object"""
    return spotipy.Spotify(
        auth_manager=spotipy.SpotifyClientCredentials(
            client_id=os.getenv("SPOTIFY_ID"),
            client_secret=os.getenv("SPOTIFY_SECRET"),
        )
    )


def get_categories(client: spotipy.Spotify, countries: list = ["US"]) -> dict:
    """Retuns all categories associated with the countries passed through"""
    all_categories_per_country = {}

    for market in countries:
        cat_resp = client.categories(country=market, limit=50)

        categories = cat_resp["categories"]["items"]
        while cat_resp["categories"]["next"]:
            cat_resp = client.next(cat_resp["categories"])
            categories.extend(cat_resp["categories"]["items"])

        all_categories_per_country[market] = categories

    return all_categories_per_country


def get_category_playlists(
    client: spotipy.Spotify, category_ids: list
) -> dict:
    all_category_playlists = {}

    for category in category_ids:
        try:
            cat_resp = client.category_playlists(category_id=category, limit=50)

            category_playlists = cat_resp["playlists"]["items"]
            while cat_resp["playlists"]["next"]:
                cat_resp = client.next(cat_resp["playlists"])
                category_playlists.extend(cat_resp["playlists"]["items"])

            all_category_playlists[category] = cat_resp
        except spotipy.SpotifyException as e:
            logging.error(e)

    return all_category_playlists


def get_name_id_artists_from_track(track_detail: dict) -> dict:
    track_info = {
            "track_id": track_detail.get("id"),
            "name": track_detail.get("name"),
            "artists": json.dumps(track_detail.get("artists"))
            }
        
    return track_info


def get_tracks_from_playlists(client: spotipy.Spotify, playlist_ids: list) -> list:
    """Pulls tracks from Spotify API using playlist endpoint"""
    tracks = []
    for pid in playlist_ids:
        try:
            playlist = client.playlist(pid)
        except spotipy.SpotifyException as e:
            logging.error(e)
            continue

        if playlist["tracks"]:
            for track in playlist["tracks"]["items"]:
                try:
                    track_info = get_name_id_artists_from_track(track["track"])
                    tracks.append(track_info)
                except Exception as e:
                    logging.error(e)
                    
            if playlist["tracks"]["next"]:
                playlist = client.next(playlist["tracks"])
                
                for track in playlist["items"]:
                    try:
                        track_info = get_name_id_artists_from_track(track["track"])
                        tracks.append(track_info)
                    except Exception as e:
                        logging.error(e)
                    
        else:
            continue
    
    return tracks


def remove_duplicate_tracks(tracklisting: List[dict]) -> List[dict]:
    track_ids = []
    unique_tracks = []
    for track in tracklisting:
        if track["track_id"] in track_ids:
            continue
        else:
            track_ids.append(track["track_id"])
            unique_tracks.append(track)
    return unique_tracks


# TODO: This function is changing as I figure out a good data flow
def main(filepath):
    logging.error("Authorizing Client")
    # client = authorize_client()
    connection = connect_to_postgres()
    # playlists = get_playlists(connection)
    # just_ids = [p["playlist_id"] for p in playlists]
    # tracks = get_tracks_from_playlists(client, just_ids)
    with open(filepath, "r") as f:
        tracks = json.load(f)
    unique_tracks = remove_duplicate_tracks(tracks)
    insert_tracks(connection, unique_tracks)
    return

if __name__ == "__main__":
    main("./tracks_20210718.json")