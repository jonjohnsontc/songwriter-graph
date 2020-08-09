import json
import logging

from sqlalchemy import between, select, func, desc, case

from songwriter_graph.db.model import writers, neighbors
from songwriter_graph.db.utils import sanitize_text

def get_writer(connection, wid):
    """Retrieves writer record from writers table, based on the WID
    
    Args:
        connection: SQLAlchemy scoped connection
        wid (int): WID for songwriter to retrieve
    
    Returns:
        Tuple representing songwriter information from writers table

    Query:
        SELECT writers.writer_name, writers.ipi
        FROM writers 
        WHERE writers.wid = {wid};
    """
    writer = select([writers.c.writer_name, writers.c.ipi])\
        .where(writers.c.wid == wid)
    
    return connection.execute(writer).fetchone().items()


def get_writers(connection, name=None):
    """Retrieves writer records from writers table, based on the name 
    passed through

    Args: 
        connection: SQLAlchemy scoped connection
        name (str): Name to search for 

    Returns:
        List of tuples representing writer records

    Query:
        SELECT writers.writer_name, writers.ipi, writers.pro 
        FROM writers 
        WHERE writers.writer_name LIKE %{name}%;
    """
    name = sanitize_text(name)

    writer_results = select([writers.c.writer_name, writers.c.ipi, writers.c.pro])\
        .where(writers.c.writer_name.like(f"%{name}%"))

    writer_results = connection.execute(writer_results).fetchall()

    return [w.items() for w in writer_results]
    


def get_neighbors(connection, wid):
    """Retrieves neighbors for a given WID
    
    Args:
        connection: SQLAlchemy scoped connection
        wid (int): WID for songwriter whose neighbors will be retrieved
    
    Returns:
        Tuple representing the 10 nearest neighbors for WID

    Query:
        SELECT
              neighbors.top_match_1
            , neighbors.top_match_2
            , neighbors.top_match_3
            , neighbors.top_match_4
            , neighbors.top_match_5
            , neighbors.top_match_6
            , neighbors.top_match_7
            , neighbors.top_match_8
            , neighbors.top_match_9
            , neighbors.top_match_10
        FROM neighbors 
        WHERE neighbors.wid = {wid};
    
    """
    neighbor_results = select([
        neighbors.c.top_match_1, 
        neighbors.c.top_match_2, 
        neighbors.c.top_match_3,
        neighbors.c.top_match_4,
        neighbors.c.top_match_5,
        neighbors.c.top_match_6,
        neighbors.c.top_match_7,
        neighbors.c.top_match_8,
        neighbors.c.top_match_9,
        neighbors.c.top_match_10])\
            .where(neighbors.c.wid == wid)
    
    neighbor_results = connection.execute(neighbor_results).fetchone().items()

    return cool_stuff
