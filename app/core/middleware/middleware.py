from flask import request, jsonify, current_app

from app.shared.utils.custom_response import ApiResponse, CustomResponse
from app.shared.utils.jwt_helper import JWTHelper
from app.shared.utils.logger import AppLogger

logger = AppLogger("JWTMiddleware")


def global_jwt_check():
    logger.info(f"Request: {request.method} {request.path}")
    excluded_paths = [
        "/api/v1/auth/access-token"
    ]
    if request.path in excluded_paths:
        return
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return CustomResponse.unauthorized(message="Token not provided")
    token = auth_header.split(" ")[1]
    try:
        decoded = JWTHelper.decode_access_token(token, secret_key=current_app.config.get("SECRET_KEY"))
        request.jwt_payload = decoded
        logger.info(f"Token validated successfully for user {decoded.get('sub', 'unknown')}")
    except Exception as e:
        logger.error(f"Token decoding failed: {str(e)}")
        return CustomResponse.unauthorized(message=f"Token invalid: '{str(e)}'.")
