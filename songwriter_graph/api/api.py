import time

from flask_restx import Resource

from songwriter_graph.api import api

#TODO: Replace this with something more robust - like what cake does
#      giving connection a default kwarg of 'None' in the queries
#      so that it can change depending upon the environment

# connection = connect(engine)

ns = app.namespace("neighbors", description="Operations related to querying Nearest Neighbors for a Writer")

@app.route('/neighbors/', methods=["GET"])
class Neighbors_endpoint(Resource):
    """Here be a doc string
    """
    get_parser = app.parser().add_argument(
        "wid",
        type=int,
        help="ID of writer to retrieve",
        required=True
    )
    @app.expect(get_parser)
    def get(self):
        args = self.get_parser.parse_args()
        result = "butt"
        return result


