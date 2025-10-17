import asyncio
from typing import Dict, Tuple

from flask import current_app
from flask_restful import Resource, reqparse
from odm_p1d.connection import create_connection

from app.modules.v1.endpoints.auth.access_token.container.login_user_container import \
    LoginUserContainer
from app.modules.v1.endpoints.auth.access_token.login_user_service import \
    LoginUserService
from app.modules.v1.endpoints.auth.access_token.model.token_request_model import \
    TokenRequest
from app.modules.v1.endpoints.auth.access_token.model.token_response_model import \
    TokenResponse
from app.shared.utils.async_resource import AsyncResource
from app.shared.utils.custom_response import ApiResponse, CustomResponse
from app.shared.utils.logger import AppLogger


class AccessTokenView(AsyncResource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "username", type=str, required=True, help="Username is mandatory"
        )
        self.parser.add_argument(
            "password", type=str, required=True, help="Password is mandatory"
        )

    async def post(self) -> ApiResponse:
        args = self.parser.parse_args()
        username: str = args.username
        password: str = args.password
        token_request: TokenRequest = TokenRequest(username=username, password=password)
        mongo_db_session = create_connection(
            db_name=current_app.config["MONGO_DB_NAME"],
            db_url=current_app.config["MONGO_DB_URL"],
        )
        login_user_container: LoginUserContainer = LoginUserContainer()
        login_user_container.mongo_session.override(mongo_db_session)
        login_user_service: LoginUserService = login_user_container.login_user_service()
        secret_key: str = current_app.config.get("SECRET_KEY")
        token_params: TokenResponse | None = await login_user_service.get_token(
            request=token_request, secret_key=secret_key
        )
        if token_params:
            return CustomResponse.ok(data=token_params.dict())
        return CustomResponse.unauthorized(message="Not authorized")
