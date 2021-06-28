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
            client_secret=os.getenv("SPOTIFY_SECRET")
        )
    )


def get_categories(client: spotipy.Spotify, countries: list=["US"]) -> dict:
    """Retuns all categories associated with the countries passed through"""
    all_categories_per_country = {}
    
    for market in countries:
        cat_resp = client.categories(country=market, limit=50)

        total_categories = cat_resp["categories"]["total"]
        while total_categories > len(cat_resp["categories"]["items"]):
            offset = len(cat_resp["categories"]["items"])
            addtl_cat_resp = client.categories(country=market, limit=50, offset=offset)
            additional_cats = addtl_cat_resp["categories"]["items"]
            cat_resp["categories"]["items"].extend(additional_cats)

        all_categories_per_country[market] = cat_resp

    return all_categories_per_country


def get_playlists(client, playlist_ids: list, ) -> list:
    return


def get_songs():
    pass


def write_out():
    pass


def main():    
    logging.error("Authorizing Client")
    client = authorize_client()
    connection = connect_to_postgres()
    logging.error("Starting to pull categories")
    categories = get_categories(client, countries=["US"])
    us_pull = json.dumps(categories)
    connection.execute(
        f"""
        INSERT INTO api_categories (data)
            VALUES ('{us_pull}')
        """)
    connection.close()
    return

main()