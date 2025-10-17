from typing import List
from dataclasses import dataclass, field


@dataclass
class ProductRecommendationModel:
    subsequences_generated: List[List[int]]
    original_subsequence: List[int] = field(default_factory=list)

    def __dict__(self):
        return {
            "original_subsequence": self.original_subsequence,
            "subsequences_generated": self.subsequences_generated
        }