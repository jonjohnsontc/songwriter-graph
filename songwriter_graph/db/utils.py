# functions to connect and retrieve data from postgres
import os

from sqlalchemy.engine import create_engine
from dotenv import load_dotenv

# TODO: Replace PG_PASSWORD with getenv
# PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DRIVER = "postgresql+psycopg2"

def connect():
    """Generates connection to postgres db
    
    Returns:
        connection object
    """
    engine = create_engine(f"{DRIVER}://postgres:{PG_PASSWORD}@localhost:5432/postgres")
    return engine.connect()



