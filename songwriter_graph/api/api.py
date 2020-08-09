import time

from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, Namespace
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from songwriter_graph.db.queries import get_neighbors, get_writers
from songwriter_graph.db.utils import CONFIG, connect, engine

app = Flask(__name__)
api = Api(
    app, 
    version="1.0", 
    title='Songwriter Graph API')

#TODO: Replace this with something more robust - like what cake does
#      giving connection a default kwarg of 'None' in the queries
#      so that it can change depending upon the environment

engine = engine()
Session = scoped_session(sessionmaker(bind=engine))
# connection = connect(engine)

@api.route('/neighbors/', methods=["GET"])
class Neighbors(Resource):
    """Here be a doc string
    """
    get_parser = api.parser().add_argument(
        "wid",
        type=int,
        help="ID of writer to retrieve",
        required=True
    )
    @api.expect(get_parser)
    def get(self):
        from flask import current_app as app
        args = self.get_parser.parse_args()
        return 


@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()

