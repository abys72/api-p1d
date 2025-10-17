from typing import List

import pytest
from odm_p1d.connection import create_connection
from testcontainers.mongodb import MongoDbContainer

from app.modules.v1.endpoints.products.create_product_recommendation.container.product_recommendation_container import \
    ProductRecommendationContainer
from app.modules.v1.endpoints.products.create_product_recommendation.model.product_recommendation_model import \
    ProductRecommendationModel
from app.modules.v1.endpoints.products.create_product_recommendation.product_recommendation_service import \
    ProductRecommendationService

TEST_DB_NAME = "test_db"


@pytest.mark.asyncio
class TestIntegrationProductRecommendation:
    @pytest.fixture(scope="function")
    def mongodb_container(self):
        with MongoDbContainer("mongo:6.0") as mongo:
            yield mongo

    @pytest.fixture
    def mongo_session(self, mongodb_container: MongoDbContainer):
        db_url: str = mongodb_container.get_connection_url()
        session = create_connection(db_name=TEST_DB_NAME, db_url=db_url)
        return session

    async def test_create_and_get_product_recommendation(self, mongo_session) -> None:
        input_sequence = [5, 7, 9]
        container: ProductRecommendationContainer = ProductRecommendationContainer()
        container.mongo_session.override(mongo_session)
        service: ProductRecommendationService = (
            container.product_recommendation_service()
        )
        await service.create_subsequence(sequence=input_sequence)

        recommendations: List[ProductRecommendationModel] | None = (
            await service.get_product_recommendation()
        )

        assert recommendations is not None
        assert len(recommendations) == 1

        recommendation = recommendations[0]

        expected_original_subsequence = [5, 7, 9]
        assert recommendation.original_subsequence == expected_original_subsequence

        expected_subsequences_generated = [
            [5],
            [7],
            [9],
            [5, 7],
            [5, 9],
            [7, 9],
            [5, 7, 9],
        ]

        actual_generated_set = set(map(tuple, recommendation.subsequences_generated))
        expected_generated_set = set(map(tuple, expected_subsequences_generated))

        assert actual_generated_set == expected_generated_set
        assert len(recommendation.subsequences_generated) == len(
            expected_subsequences_generated
        )
