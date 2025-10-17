import asyncio
from typing import Coroutine

from odm_p1d.collection.user import User

from app.modules.v1.endpoints.auth.access_token.protocol.login_user_query_protocol import \
    LoginUserQueryProtocol
from app.shared.utils.logger import AppLogger


class LoginUserRepository:
    __login_user_query: LoginUserQueryProtocol
    __logger: AppLogger

    def __init__(
        self, logger: AppLogger, login_user_query: LoginUserQueryProtocol
    ) -> None:
        self.__logger = logger
        self.__login_user_query = login_user_query

    async def find_by_credentials(self, username: str, password: str) -> bool:
        try:
            user: User | None = await self.__login_user_query.find_by_credentials(
                username, password
            )
            if user:
                self.__logger.info(f"User found. '{username}' authenticated.")
                return True
            return False
        except Exception as e:
            self.__logger.error(f"Failed to authenticate user: {str(e)}")
            return False
