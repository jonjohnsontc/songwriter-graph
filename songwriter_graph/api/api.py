import time
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from songwriter_graph.db.queries import get_neighbors, get_writers
from songwriter_graph.db.utils import connect

app = Flask(__name__)
api = Api(app)

#TODO: Replace this with something more robust - like what cake does
#      giving connection a default kwarg of 'None' in the queries
#      so that it can change depending upon the environment
connection = connect()

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
    def get(self):
        args = self.get_parser.parse_args()
        neighbors = get_neighbors(connection, args.wid)
        return neighbors

if __name__ == '__main__':
    app.run(debug=True)