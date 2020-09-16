from flask_restx import Api

from songwriter_graph.web.apis.api import Neighbors_endpoint as neighbors

api = Api( 
    version="1.0", 
    title='Songwriter Graph API')
api.add_namespace(neighbors)
