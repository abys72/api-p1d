from typing import Protocol

from odm_p1d.collection.user import User


class LoginUserQueryProtocol(Protocol):

    async def find_by_credentials(self, username: str, password: str) -> User | None:
        ...
