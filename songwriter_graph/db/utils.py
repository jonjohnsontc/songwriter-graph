# functions to connect and retrieve data from postgres
import json
import os

from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
load_dotenv()

PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DRIVER = "postgresql+psycopg2"

def connect():
    """Generates connection to postgres db
    
    Returns:
        connection object
    """
    engine = create_engine(f"{DRIVER}://postgres:{PG_PASSWORD}@localhost:5432/postgres")
    return engine.connect()

#TODO: Either do something with or delete
def sanitize_text(text):
    return text


def to_json():
    pass