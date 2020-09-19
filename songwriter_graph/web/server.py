from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from songwriter_graph.web.apis import api
from songwriter_graph.db.utils import read_config

CONFIG = read_config("/Users/jonjohnson/dev/swg/Song_Index/songwriter_graph/config.json")

app = Flask(__name__)
app.config.from_mapping(CONFIG)
db = SQLAlchemy(app)
api.init_app(app)

