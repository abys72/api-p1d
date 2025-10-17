from itertools import combinations
from typing import List

from app.modules.v1.endpoints.products.create_product_recommendation.model.product_recommendation_model import \
    ProductRecommendationModel
from app.modules.v1.endpoints.products.create_product_recommendation.repository.product_recommendation_repository import \
    ProductRecommendationRepository
from app.shared.utils.logger import AppLogger


class ProductRecommendationService:
    __product_recommendation_repository: ProductRecommendationRepository
    __logger: AppLogger

    def __init__(self, product_recommendation_repository: ProductRecommendationRepository, logger: AppLogger) -> None:
        self.__product_recommendation_repository = product_recommendation_repository
        self.__logger = logger

    async def create_subsequence(self, sequence: List[int]) -> None:
        try:
            subsequences: List[List[int]] | None = self._create_subsequences(sequence)
            if subsequences is None:
                return None
            recommendation_model = ProductRecommendationModel(
                subsequences_generated=subsequences
            )
            await self.__product_recommendation_repository.insert_product_recommendation(recommendation_model)
        except Exception as e:
            self.__logger.error(f"Error while creating subsequence for sequence '{sequence}': '{e}'.")
            raise e
        return None

    async def get_product_recommendation(self) -> List[ProductRecommendationModel] | None:
        try:
            recommendations_models: List[
                ProductRecommendationModel] = await self.__product_recommendation_repository.get_product_recommendations()
            if recommendations_models is None or len(recommendations_models) == 0:
                self.__logger.info(f"No models found: '{recommendations_models}'.")
                return None
            recommendations_models_with_original: List[ProductRecommendationModel] = self._find_subsequence(
                subsequence=recommendations_models)
            return recommendations_models_with_original
        except Exception as e:
            self.__logger.error(f"Error getting product recommendation: '{e}'.")
            return None

    def _create_subsequences(self, sequence: List[int]) -> List[List[int]] | None:
        result_subsequence: List[List[int]] = []
        try:
            for i in range(1, len(sequence) + 1):
                for combi in combinations(sequence, i):
                    result_subsequence.append(list(combi))
            sorted_subsequences: List[List[int]] = sorted(result_subsequence, key=lambda s: (len(s), s))
        except Exception as e:
            self.__logger.error(f"Error generating subsequence: '{e}'.")
            return None
        return sorted_subsequences

    def _find_subsequence(self, subsequence: List[
        ProductRecommendationModel]) -> List[ProductRecommendationModel]:
        for sequence in subsequence:
            original_subsequence: List[int] = max(sequence.subsequences_generated, key=len)
            sequence.original_subsequence = original_subsequence
        return subsequence
