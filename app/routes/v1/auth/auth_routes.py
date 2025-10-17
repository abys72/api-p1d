from flask_restful import Api

from app.modules.v1.endpoints.auth.access_token.view import AccessTokenView


def register_auth_routes(app):
    api = Api(app, prefix="/api/v1/auth")
    api.add_resource(AccessTokenView, "/access-token")
