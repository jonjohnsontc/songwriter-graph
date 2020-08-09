import time

from flask import Flask, Blueprint, jsonify
from flask_restx import Resource, Api, Namespace
from flask_sqlalchemy import SQLAlchemy

from songwriter_graph.db.queries import get_neighbors, get_writers
from songwriter_graph.db.utils import CONFIG, connect, engine

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint, 
    version="1.0", 
    title='Songwriter Graph API')

db = SQLAlchemy()

ns = Namespace('neighbors', description='Get a list of neighbors for a given wid')

def build_app(config=CONFIG):
    app = Flask(__name__)
    app.config.from_mapping(config)
    app.register_blueprint(blueprint)
    db.init_app(app)

    with app.app_context():
        api.add_namespace(ns)
    return app

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
        # args = self.get_parser.parse_args()
        binds = db.get_binds(app)
        # connection = db.get_engine(app)
        # neighbors = get_neighbors(connection, args.wid)
        return f"{binds}"

#TODO: Replace this with something more robust - like what cake does
#      giving connection a default kwarg of 'None' in the queries
#      so that it can change depending upon the environment

# engine = engine()
# connection = connect(engine)