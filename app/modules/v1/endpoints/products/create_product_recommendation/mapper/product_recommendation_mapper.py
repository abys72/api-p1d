from typing import List

from app.modules.v1.endpoints.products.create_product_recommendation.model.product_recommendation_model import \
    ProductRecommendationModel
from odm_p1d.collection.subsequence import Subsequence


class ProductRecommendationMapper:

    @staticmethod
    def map_get_subsequences(data: List[Subsequence]) -> List[ProductRecommendationModel]:
        return [
            ProductRecommendationModel(subsequences_generated=item.subsequence)
            for item in data
        ]

    @staticmethod
    def map_insert_subsequences(data: ProductRecommendationModel) -> Subsequence:
        return Subsequence(subsequence=data.subsequences_generated)
