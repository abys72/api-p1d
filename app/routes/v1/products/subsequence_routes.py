from flask_restful import Api

from app.modules.v1.endpoints.products.create_product_recommendation.view import \
    SubsequenceView


def register_subsequences_routes(app):
    api = Api(app, prefix="/api/v1/subsequence")
    api.add_resource(SubsequenceView, "/create", "/get")
