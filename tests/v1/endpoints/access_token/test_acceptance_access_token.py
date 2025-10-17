from typing import Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.modules.v1.endpoints.auth.access_token.container.login_user_container import \
    LoginUserContainer
from app.modules.v1.endpoints.auth.access_token.login_user_service import \
    LoginUserService
from app.modules.v1.endpoints.auth.access_token.model.token_request_model import \
    TokenRequest
from app.modules.v1.endpoints.auth.access_token.model.token_response_model import \
    TokenResponse


@pytest.mark.asyncio
class TestAcceptanceAccessToken:

    @pytest.fixture
    def auth_service(self) -> LoginUserService:
        mongo_db_session = AsyncMock()
        login_user_container: LoginUserContainer = LoginUserContainer()
        login_user_container.mongo_session.override(mongo_db_session)

        return login_user_container.login_user_service()

    async def test_access_token_response_user_incorrect(
        self, auth_service: LoginUserService
    ) -> None:
        with patch.object(
            auth_service._user_repository, "find_by_credentials", new_callable=AsyncMock
        ) as mock_find_by_credentials:
            mock_find_by_credentials.return_value = False
            token_request: TokenRequest = TokenRequest(
                username="Test1", password="Error"
            )
            token_params: TokenResponse | None = await auth_service.get_token(
                request=token_request, secret_key="secret"
            )
            assert token_params is None

    async def test_access_token_input_correct(
        self, auth_service: LoginUserService
    ) -> None:
        with patch.object(
            auth_service._user_repository, "find_by_credentials", new_callable=AsyncMock
        ) as mock_find_by_credentials:
            mock_find_by_credentials.return_value = True
            with patch(
                "app.modules.v1.endpoints.auth.access_token.login_user_service.JWTHelper.create_access_token"
            ) as mock_create_token:
                expected_token_dict = {
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiAiYWRtaW4iLCAiaW",
                    "expires_at": 1234567890,
                }
                mock_create_token.return_value = expected_token_dict

                token_request = TokenRequest(username="admin", password="hola123")
                token_params: TokenResponse | None = await auth_service.get_token(
                    request=token_request, secret_key="secret"
                )

                assert token_params is not None
                assert token_params.dict() == expected_token_dict
                assert "access_token" in token_params.dict()
                assert "expires_at" in token_params.dict()
                mock_create_token.assert_called_once_with(
                    identity="admin", secret_key="secret"
                )
