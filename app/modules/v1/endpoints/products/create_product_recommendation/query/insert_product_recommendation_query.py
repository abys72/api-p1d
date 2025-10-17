from odmantic.typing import Any

from odm_p1d.collection.subsequence import Subsequence

from app.shared.utils.logger import AppLogger


class InsertProductRecommendationQuery:
    __session: Any
    __logger: AppLogger

    def __init__(self, session: Any, logger: AppLogger):
        self.__session = session
        self.__logger = logger

    async def insert_product_recommendation(self, product_recommendation_model: Subsequence) -> None:
        self.__logger.info(f"Inserting product recommendation: '{product_recommendation_model.__dict__}'.")
        try:
            await self.__session.save(product_recommendation_model)
            self.__logger.info("All insert subsequence operations inserted.")
        except Exception as e:
            self.__logger.info(f"Error inserting product_recommendation_model '{e}'.")
            raise e
