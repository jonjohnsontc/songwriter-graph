from typing import List
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
    categories: List[dict] = category[country_code]['categories']['items']

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