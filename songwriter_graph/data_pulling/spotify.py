import json
import logging
import os
import psycopg2
import spotipy

from sqlalchemy.engine import create_engine
from dotenv import load_dotenv

load_dotenv("/Users/jonjohnson/dev/swg/Song_Index/.env")


def connect_to_postgres():
    # postgresql+psycopg2://user:password@host:port/dbname
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

        total_categories = cat_resp["categories"]["total"]
        while total_categories > len(cat_resp["categories"]["items"]):
            offset = len(cat_resp["categories"]["items"])
            addtl_cat_resp = client.categories(
                country=market, limit=50, offset=offset
            )
            additional_cats = addtl_cat_resp["categories"]["items"]
            cat_resp["categories"]["items"].extend(additional_cats)

        all_categories_per_country[market] = cat_resp

    return all_categories_per_country


def get_category_playlists(
    client: spotipy.Spotify, category_ids: list
) -> dict:
    all_category_playlists = {}

    for category in category_ids:
        cat_resp = client.category_playlists(category_id=category, limit=50)

        total_cat_playlists = cat_resp["categories"]["total"]
        while total_cat_playlists > len(cat_resp["categories"]["items"]):
            offset = len(cat_resp["categories"]["items"])
            additional_cat_resp = client.category_playlists(
                category_id=category, offset=offset, limit=50
            )
            addtl_cat_playlists = additional_cat_resp["categories"]["items"]
            additional_cat_resp["categories"]["items"].extend(
                addtl_cat_playlists
            )

        all_category_playlists[category] = cat_resp

    return all_category_playlists


def get_songs():
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


main()
