from typing import List

from odm_p1d.collection.subsequence import Subsequence


class MockGetProductRecommendationQuery:
    async def get_subsequences(self) -> List[Subsequence]:
        return [
            Subsequence(subsequence=[[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]),
            Subsequence(subsequence=[[1], [2], [1, 2]]),
            Subsequence(
                subsequence=[
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
                ]
            ),
            Subsequence(subsequence=[[5], [7], [9], [5, 7], [5, 9], [7, 9], [5, 7, 9]]),
        ]
