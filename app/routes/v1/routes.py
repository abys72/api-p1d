from app.routes.v1.auth.auth_routes import register_auth_routes
from app.routes.v1.products.subsequence_routes import \
    register_subsequences_routes


def register_routes(app):
    register_auth_routes(app)
    # register_users_routes(app)
    register_subsequences_routes(app)
