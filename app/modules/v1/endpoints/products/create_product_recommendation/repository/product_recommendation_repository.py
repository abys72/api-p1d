import asyncio
from typing import List

from odm_p1d.collection.subsequence import Subsequence

from app.modules.v1.endpoints.products.create_product_recommendation.mapper.product_recommendation_mapper import \
    ProductRecommendationMapper
from app.modules.v1.endpoints.products.create_product_recommendation.model.product_recommendation_model import \
    ProductRecommendationModel
from app.modules.v1.endpoints.products.create_product_recommendation.protocols.product_recommendation_query_protocol import (
    GetProductRecommendationQueryProtocol,
    InsertProductRecommendationQueryProtocol)
from app.shared.utils.logger import AppLogger


class ProductRecommendationRepository:
    __logger: AppLogger
    __product_recommendation_mapper: ProductRecommendationMapper
    __insert_product_recommendations_query_protocol: (
        InsertProductRecommendationQueryProtocol
    )
    __get_product_recommendations_query_protocol: GetProductRecommendationQueryProtocol

    def __init__(
        self,
        logger: AppLogger,
        product_recommendation_mapper: ProductRecommendationMapper,
        get_product_recommendations_query_protocol: GetProductRecommendationQueryProtocol,
        insert_product_recommendations_query_protocol: InsertProductRecommendationQueryProtocol,
    ):
        self.__logger = logger
        self.__product_recommendation_mapper = product_recommendation_mapper
        self.__insert_product_recommendations_query_protocol = (
            insert_product_recommendations_query_protocol
        )
        self.__get_product_recommendations_query_protocol = (
            get_product_recommendations_query_protocol
        )

    async def insert_product_recommendation(
        self, recommendation_ids: ProductRecommendationModel
    ) -> None:
        self.__logger.info(
            f"Inserting product recommendations: '{recommendation_ids}'."
        )
        odm_recommendation_model: Subsequence = (
            self.__product_recommendation_mapper.map_insert_subsequences(
                data=recommendation_ids
            )
        )
        await self.__insert_product_recommendations_query_protocol.insert_product_recommendation(
            product_recommendation_model=odm_recommendation_model
        )

    async def get_product_recommendations(self) -> List[ProductRecommendationModel]:
        self.__logger.info("Getting subsequences.")
        list_of_subsequence: List[Subsequence] = (
            await self.__get_product_recommendations_query_protocol.get_subsequences()
        )
        list_product_recommendations: List[ProductRecommendationModel] = (
            self.__product_recommendation_mapper.map_get_subsequences(
                data=list_of_subsequence
            )
        )
        return list_product_recommendations
