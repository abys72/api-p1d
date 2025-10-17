from typing import List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from odm_p1d.collection.subsequence import Subsequence

from app.modules.v1.endpoints.products.create_product_recommendation.container.product_recommendation_container import \
    ProductRecommendationContainer
from app.modules.v1.endpoints.products.create_product_recommendation.model.product_recommendation_model import \
    ProductRecommendationModel
from app.modules.v1.endpoints.products.create_product_recommendation.product_recommendation_service import \
    ProductRecommendationService
from tests.v1.endpoints.create_product_recommendation.mock_get_product_recommendation_query import \
    MockGetProductRecommendationQuery
from tests.v1.endpoints.create_product_recommendation.mock_insert_product_recommendation_query import \
    MockInsertProductRecommendationQuery


@pytest.mark.asyncio
class TestAcceptanceCreateProductRecommendation:

    @pytest.fixture
    def mongo_session(self) -> MagicMock:
        mongo_session = MagicMock()
        return mongo_session

    @pytest.fixture
    def product_recommendation_container(
        self, mongo_session: MagicMock
    ) -> ProductRecommendationContainer:
        get_product_recommendation_query: MockGetProductRecommendationQuery = (
            MockGetProductRecommendationQuery()
        )
        insert_product_recommendation_query: MockInsertProductRecommendationQuery = (
            MockInsertProductRecommendationQuery()
        )
        product_recommendation_container: ProductRecommendationContainer = (
            ProductRecommendationContainer()
        )
        product_recommendation_container.mongo_session.override(mongo_session)
        product_recommendation_container.insert_product_recommendation_query.override(
            insert_product_recommendation_query
        )
        product_recommendation_container.get_product_recommendation_query.override(
            get_product_recommendation_query
        )
        return product_recommendation_container

    async def test_create_product_recommendation(
        self, product_recommendation_container: ProductRecommendationContainer
    ) -> None:
        path_to_patch = (
            "tests.v1.endpoints.create_product_recommendation.mock_insert_product_recommendation_query."
            "MockInsertProductRecommendationQuery.insert_product_recommendation"
        )
        with patch(
            path_to_patch, new_callable=AsyncMock
        ) as insert_product_recommendation_mock:
            subsequence_input: List[int] = [2, 3, 4]
            expected_subsequence: Subsequence = Subsequence(
                subsequence=[[2], [3], [4], [2, 3], [2, 4], [3, 4], [2, 3, 4]]
            )

            service: ProductRecommendationService = (
                product_recommendation_container.product_recommendation_service()
            )
            await service.create_subsequence(sequence=subsequence_input)
            subsequence_obj: Subsequence = (
                insert_product_recommendation_mock.call_args_list[0][1][
                    "product_recommendation_model"
                ]
            )

            insert_product_recommendation_mock.assert_called_once()
            assert isinstance(subsequence_obj, Subsequence)
            assert subsequence_obj.subsequence == expected_subsequence.subsequence
            assert len(subsequence_obj.subsequence) == len(
                expected_subsequence.subsequence
            )

    async def test_get_product_recommendation(
        self, product_recommendation_container: ProductRecommendationContainer
    ) -> None:
        expected_product_recommendation: List[ProductRecommendationModel] = [
            ProductRecommendationModel(
                original_subsequence=[1, 2, 3],
                subsequences_generated=[
                    [1],
                    [2],
                    [3],
                    [1, 2],
                    [1, 3],
                    [2, 3],
                    [1, 2, 3],
                ],
            ),
            ProductRecommendationModel(
                original_subsequence=[1, 2], subsequences_generated=[[1], [2], [1, 2]]
            ),
            ProductRecommendationModel(
                original_subsequence=[1, 2, 3, 4],
                subsequences_generated=[
                    [1],
                    [2],
                    [3],
                    [4],
                    [1, 2],
                    [1, 3],
                    [1, 4],
                    [2, 3],
                    [2, 4],
                    [3, 4],
                    [1, 2, 3],
                    [1, 2, 4],
                    [1, 3, 4],
                    [2, 3, 4],
                    [1, 2, 3, 4],
                ],
            ),
            ProductRecommendationModel(
                original_subsequence=[5, 7, 9],
                subsequences_generated=[
                    [5],
                    [7],
                    [9],
                    [5, 7],
                    [5, 9],
                    [7, 9],
                    [5, 7, 9],
                ],
            ),
        ]
        service: ProductRecommendationService = (
            product_recommendation_container.product_recommendation_service()
        )

        result_product_recommendations: List[ProductRecommendationModel] = (
            await service.get_product_recommendation()
        )

        assert result_product_recommendations == expected_product_recommendation
        assert len(result_product_recommendations) == len(
            expected_product_recommendation
        )
