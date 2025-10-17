import pytest
from typing import List

from odm_p1d.collection.user import User
from odm_p1d.connection import create_connection
from testcontainers.mongodb import MongoDbContainer

from app.modules.v1.endpoints.auth.access_token.container.login_user_container import LoginUserContainer
from app.modules.v1.endpoints.auth.access_token.login_user_service import LoginUserService
from app.modules.v1.endpoints.auth.access_token.model.token_request_model import TokenRequest
from app.modules.v1.endpoints.auth.access_token.model.token_response_model import TokenResponse

TEST_DB_NAME = "test_db"


@pytest.mark.asyncio
class TestIntegrationAccessToken:
    @pytest.fixture(scope="function")
    def mongodb_container(self):
        with MongoDbContainer("mongo:6.0") as mongo:
            yield mongo

    @pytest.fixture
    def mongo_session(self, mongodb_container: MongoDbContainer):
        db_url: str = mongodb_container.get_connection_url()
        session = create_connection(db_name=TEST_DB_NAME, db_url=db_url)
        return session

    async def test_access_token_incorrect_user_password(self, mongo_session) -> None:
        users: User = User(name="test", email="test@email.com", password="test")
        await mongo_session.save(users)
        login_user_container: LoginUserContainer = LoginUserContainer()
        login_user_container.mongo_session.override(mongo_session)

        auth_service: LoginUserService = login_user_container.login_user_service()
        user: TokenRequest = TokenRequest(username="test@email.com", password="13213213213")
        response_user: TokenResponse | None = await auth_service.get_token(user, secret_key="123")

        assert response_user is None

    async def test_access_token_correct_user_password(self, mongo_session) -> None:
        users: User = User(name="test", email="test@email.com", password="test")
        await mongo_session.save(users)
        login_user_container: LoginUserContainer = LoginUserContainer()
        login_user_container.mongo_session.override(mongo_session)

        auth_service: LoginUserService = login_user_container.login_user_service()
        user: TokenRequest = TokenRequest(username="test", password="test")
        response_user: TokenResponse | None = await auth_service.get_token(user, secret_key="123")

        assert response_user is not None