from flask import Flask, jsonify

from app.core.config import Config
from app.core.middleware.middleware import global_jwt_check
from app.routes.v1.routes import register_routes
from app.shared.utils.custom_response import CustomResponse


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.before_request(global_jwt_check)
    register_routes(app)

    @app.errorhandler(404)
    def handle_404(error):
        return CustomResponse.not_found(message="Resource not found")

    @app.errorhandler(405)
    def handle_405(error):
        return CustomResponse.not_found(message="Resource not found")

    return app
