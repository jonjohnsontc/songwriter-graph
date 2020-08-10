import time

from flask_restx import Resource
from flask_sqlalchemy import SQLAlchemy

from songwriter_graph.api import api
from songwriter_graph.db.model import Neighbors, Writers
from songwriter_graph.db.queries import get_neighbors, get_writers
from songwriter_graph.db.utils import CONFIG, connect, engine

#TODO: Replace this with something more robust - like what cake does
#      giving connection a default kwarg of 'None' in the queries
#      so that it can change depending upon the environment

engine = engine()
# connection = connect(engine)

ns = api.namespace("neighbors", description="Operations related to querying Nearest Neighbors for a Writer")

@api.route('/neighbors/', methods=["GET"])
class Neighbors_endpoint(Resource):
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
        args = self.get_parser.parse_args()
        result = Neighbors.query.filter(Neighbors.wid == args.wid)
        return result


