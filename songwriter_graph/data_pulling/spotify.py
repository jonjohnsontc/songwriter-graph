import json
import logging
import os
import psycopg2
import spotipy

from sqlalchemy.engine import create_engine
from dotenv import load_dotenv

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
            cat_resp = client.next(cat_resp)
            categories.extend(cat_resp["categories"]["items"])

        all_categories_per_country[market] = categories

    return all_categories_per_country


def get_category_playlists(
    client: spotipy.Spotify, category_ids: list
) -> dict:
    all_category_playlists = {}

    for category in category_ids:
        cat_resp = client.category_playlists(category_id=category, limit=50)

        category_playlists = cat_resp["playlists"]["items"]
        while cat_resp["playlists"]["next"]:
            cat_resp = client.next(cat_resp)
            category_playlists.extend(cat_resp["categories"]["items"])

        all_category_playlists[category] = cat_resp

    return all_category_playlists


def get_tracks_from_playlist(client: spotipy.Spotify, playlist: dict) -> list:
    pass


def write_out():
    pass


def main():
    logging.error("Authorizing Client")
    client = authorize_client()
    connection = connect_to_postgres()
    logging.error("Starting to pull category playlists")
    category_playlists = get_category_playlists(client, category_ids=None)
    us_pull = json.dumps(category_playlists)
    logging.error("Writing to SQL")
    connection.execute(
        f"""
        INSERT INTO api_category_playlists (data)
            VALUES ('{us_pull}')
        """
    )
    connection.close()
    return