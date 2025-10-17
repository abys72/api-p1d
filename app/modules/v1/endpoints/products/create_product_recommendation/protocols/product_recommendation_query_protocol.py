from typing import Any, Coroutine, List, Protocol

from odm_p1d.collection.subsequence import Subsequence


class InsertProductRecommendationQueryProtocol(Protocol):
    def insert_product_recommendation(
        self, product_recommendation_model: Subsequence
    ) -> Coroutine[Any, Any, None]: ...


class GetProductRecommendationQueryProtocol(Protocol):
    def get_subsequences(self) -> Coroutine[Any, Any, List[Subsequence]]: ...
