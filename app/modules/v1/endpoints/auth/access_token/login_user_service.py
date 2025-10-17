from typing import Dict

from app.modules.v1.endpoints.auth.access_token.model.token_request_model import TokenRequest
from app.modules.v1.endpoints.auth.access_token.model.token_response_model import TokenResponse
from app.modules.v1.endpoints.auth.access_token.repository.login_user_repository import LoginUserRepository
from app.shared.utils.jwt_helper import JWTHelper
from app.shared.utils.logger import AppLogger


class LoginUserService:
    _user_repository: LoginUserRepository
    _logger: AppLogger

    def __init__(self, user_repository: LoginUserRepository, logger: AppLogger):
        self._user_repository = user_repository
        self._logger = logger

    async def get_token(self, request: TokenRequest, secret_key: str) -> TokenResponse | None:
        self._logger.info(f"Login attempt for username: {request.username}")
        is_valid_user: bool = await self._user_repository.find_by_credentials(request.username, request.password)
        if is_valid_user:
            token_params: Dict[str, str | int] = JWTHelper.create_access_token(identity=request.username,
                                                                               secret_key=secret_key)
            self._logger.info(f"Token generated for user: {request.username}")
            return TokenResponse(
                access_token=token_params['access_token'],
                expires_at=token_params['expires_at']
            )
        self._logger.warning(f"Failed login attempt for username: {request.username}")
        return None
