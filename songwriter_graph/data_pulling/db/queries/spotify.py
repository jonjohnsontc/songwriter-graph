import json

from typing import List, Union
from sqlalchemy.sql.expression import text
from sqlalchemy.engine import Connection
from sqlalchemy.engine.result import ResultProxy

def get_category_result(connection: Connection, _id: int, country_code: str) -> List[dict]:
    """Retrieve category listing from db"""
    sql_stmt = f"""
        SELECT data -> '{country_code}'
        FROM api_categories
        WHERE id = {_id}
        """
    results: ResultProxy = connection.execute(sql_stmt)
    
    # pulling from Result->RowProxy to retrieve original json
    category: dict = results.next().values()[0]
    categories: List[dict] = category['categories']['items']

    return categories


def insert_category_result(connection: Connection, data: dict) -> None:
    """Send category listing from api to db"""
    sql_stmt = f"""
        INSERT INTO api_category_playlists (data)
            VALUES ('{data}')
        """
    connection.execute(sql_stmt)
    return


def get_category_playlist_result(connection: Connection, _id: int) -> list:
    return


def set_category_playlist_result(connection: Connection, data: dict) -> list:
    return


def insert_playlist(connection: Connection, playlist_record: dict) -> None:
    sql_stmt = f"""
        INSERT INTO playlists (playlist_id, snapshot_id, uri)
            VALUES (
                {playlist_record["playlist_id"]}, 
                {playlist_record["snapshot_id"]},
                {playlist_record["category_id"]},
                {playlist_record["uri"]})
        """
    connection.execute(sql_stmt)
    return


def insert_playlists(conn: Connection, playlists: list) -> None:
    sql_stmt = text(
        """INSERT INTO playlists (playlist_id, playlist_name, snapshot_id, uri)
            VALUES (:playlist_id, :playlist_name, :snapshot_id, :uri)"""
            )

    conn.execute(sql_stmt, playlists)
    return


def get_playlists(conn: Connection, playlist_name: Union[str,None]=None) -> List[dict]:
    if playlist_name:
        sql_stmt = f"""
        SELECT DISTINCT playlist_id, playlist_name 
        FROM playlists
        WHERE playlist_name = {playlist_name}
        """
    else:
        sql_stmt = f"""
        SELECT DISTINCT playlist_id, playlist_name 
        FROM playlists
        """
    results: ResultProxy = conn.execute(sql_stmt)
    playlists = results.fetchall()
    playlists = [{"playlist_id": f[0], "playlist_name": f[1]} for f in playlists]
    return playlists


def insert_tracks(conn: Connection, tracks: List[dict]) -> None:
    
    # In previous versions of `get_tracks_from_playlists`,
    # each `artists` dictionary in tracks needed to be changed into a json string
    # for track in tracks:
        # track["artists"] = json.dumps(track["artists"])

    sql_stmt = text(
        f"""INSERT INTO tracks (track_id, track_name, artists)
                VALUES (:track_id, :name, :artists)
        """
        )
    conn.execute(sql_stmt, tracks)
    return


def get_tracks(conn: Connection, track_ids: Union[List[str],None]=None) -> None:
    return