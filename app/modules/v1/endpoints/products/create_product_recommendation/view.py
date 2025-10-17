import asyncio
import os
from typing import Dict, Tuple, List

from odm_p1d.connection import create_connection
from flask_restful import Resource, reqparse

from app.modules.v1.endpoints.products.create_product_recommendation.container.product_recommendation_container import \
    ProductRecommendationContainer
from app.modules.v1.endpoints.products.create_product_recommendation.model.product_recommendation_model import \
    ProductRecommendationModel
from app.shared.utils.async_resource import AsyncResource
from app.shared.utils.custom_response import CustomResponse, ApiResponse
from app.shared.utils.logger import AppLogger
from flask import current_app


class SubsequenceView(AsyncResource):

    async def post(self) -> ApiResponse:
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('sequence', type=list, required=True, location='json', help="sequence is mandatory")
            args = parser.parse_args()
            sequence: List = args.sequence
            if not isinstance(sequence, List) and not all(isinstance(x, int) for x in sequence):
                return CustomResponse.bad_request(
                    message=f"Sequence must be a list or a list with no negative int '{sequence}'.")
            mongo_db_session = create_connection(db_name=current_app.config["MONGO_DB_NAME"],
                                                 db_url=current_app.config["MONGO_DB_URL"])
            product_recommendation_container: ProductRecommendationContainer = ProductRecommendationContainer()
            product_recommendation_container.mongo_session.override(mongo_db_session)
            product_recommendation_service = product_recommendation_container.product_recommendation_service()
            await product_recommendation_service.create_subsequence(sequence)
            return CustomResponse.ok(data={"sequence": sequence},
                                     message="Subsequence created successfully")
        except Exception as e:
            return CustomResponse.server_error(message=f"An error occurred while creating subsequence. '{str(e)}'.")

    async def get(self) -> ApiResponse:
        try:
            mongo_db_session = create_connection(db_name=current_app.config["MONGO_DB_NAME"],
                                                 db_url=current_app.config["MONGO_DB_URL"])
            product_recommendation_container: ProductRecommendationContainer = ProductRecommendationContainer()
            product_recommendation_container.mongo_session.override(mongo_db_session)
            product_recommendation_service = product_recommendation_container.product_recommendation_service()

            recommendations: List[
                                 ProductRecommendationModel] | None = await product_recommendation_service.get_product_recommendation()

            if recommendations is None:
                return CustomResponse.ok(
                    message="No recommendations found",
                    data={"recommendations": []}
                )
            recommendations_data: List[Dict] = [rec.__dict__() for rec in recommendations]
            return CustomResponse.ok(data=recommendations_data)
        except Exception as e:
            return CustomResponse.server_error(message=f"Error retrieving recommendations '{str(e)}'.")
