from odm_p1d.collection.user import User
from odmantic.typing import Any

from app.shared.utils.logger import AppLogger


class LoginUserQuery:
    __logger: AppLogger
    __session: Any

    def __init__(self, logger: AppLogger, session: Any) -> None:
        self.__logger = logger
        self.__session = session

    async def find_by_credentials(self, username: str, password: str) -> User | None:
        try:
            user: User | None = await self.__session.find_one(
                User, User.name == username, User.password == password
            )
            if user is None:
                self.__logger.warning(f"No user found with username '{username}'.")
            return user
        except Exception as e:
            self.__logger.error(f"Error finding user: '{e}'.")
            return None
