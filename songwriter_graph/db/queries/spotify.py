from typing import List
from sqlalchemy.engine import Connection
from sqlalchemy.engine.result import ResultProxy


def get_category_result(connection: Connection, _id: int) -> List[dict]:
    """Retrieve category listing from db"""
    sql_stmt = f"""
        SELECT data
        FROM api_categories
        WHERE id = {_id}
        """
    results: ResultProxy = connection.execute(sql_stmt)
    return
