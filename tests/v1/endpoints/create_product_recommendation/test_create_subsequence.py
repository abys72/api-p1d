from typing import List
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.v1.endpoints.products.create_product_recommendation.product_recommendation_service import \
    ProductRecommendationService


class TestCreateSubsequence:

    @pytest.fixture
    def product_recommendation_service(self) -> ProductRecommendationService:
        logger: MagicMock = MagicMock()
        product_recommendation_repository: AsyncMock = AsyncMock()
        service = ProductRecommendationService(
            logger, product_recommendation_repository
        )
        return service

    def test_create_subsequence(
        self, product_recommendation_service: ProductRecommendationService
    ) -> None:
        expected_subsequence: List[List[int]] = [[1], [2], [1, 2]]
        sequence: List[int] = [1, 2]

        result_subsequence: List[List[int]] = (
            product_recommendation_service._create_subsequences(sequence)
        )
        assert len(result_subsequence) == len(expected_subsequence)
        for subsequence in result_subsequence:
            assert subsequence in expected_subsequence
        assert result_subsequence == expected_subsequence
