import json
import os
from pathlib import Path

from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
load_dotenv()

PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DRIVER = "postgresql+psycopg2"


def read_config(config_path):
    with open(config_path) as f:
        config = json.load(f)

    config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"].replace("password", PG_PASSWORD)
    return config


def engine():
    return create_engine(f"{DRIVER}://postgres:{PG_PASSWORD}@localhost:5432/postgres")


def connect(engine):
    """Generates connection to postgres db
    
    Returns:
        connection object
    """
    return engine.connect()


#TODO: Either do something with or delete
def sanitize_text(text):
    return text


def to_json():
    pass


CONFIG = read_config(Path("/Users/jonjohnson/dev/swg/Song_Index/songwriter_graph/config.json"))