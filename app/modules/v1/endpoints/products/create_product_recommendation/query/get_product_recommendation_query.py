from typing import List

from odm_p1d.collection.subsequence import Subsequence
from odmantic import query
from odmantic.typing import Any
from pymongo import DESCENDING

from app.shared.utils.logger import AppLogger


class GetProductRecommendationQuery:
    __session: Any
    __logger: AppLogger

    def __init__(self, session: Any, logger: AppLogger):
        self.__session = session
        self.__logger = logger

    async def get_subsequences(self) -> List[Subsequence]:
        self.__logger.info("Fetching last 10 subsequences")
        try:
            subsequences = await self.__session.find(
                Subsequence, sort=query.desc(Subsequence.created_at), limit=10
            )
            self.__logger.info(f"subsequences '{subsequences}'.")
            return subsequences
        except Exception as e:
            self.__logger.error(f"Error getting subsequences: '{e}'-.")
            raise e
