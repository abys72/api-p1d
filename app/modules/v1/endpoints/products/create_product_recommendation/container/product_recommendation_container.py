from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory, Singleton

from app.modules.v1.endpoints.products.create_product_recommendation.mapper.product_recommendation_mapper import \
    ProductRecommendationMapper
from app.modules.v1.endpoints.products.create_product_recommendation.product_recommendation_service import \
    ProductRecommendationService
from app.modules.v1.endpoints.products.create_product_recommendation.query.get_product_recommendation_query import \
    GetProductRecommendationQuery
from app.modules.v1.endpoints.products.create_product_recommendation.query.insert_product_recommendation_query import \
    InsertProductRecommendationQuery
from app.modules.v1.endpoints.products.create_product_recommendation.repository.product_recommendation_repository import \
    ProductRecommendationRepository
from app.shared.utils.logger import AppLogger


class ProductRecommendationContainer(DeclarativeContainer):
    mongo_session = Dependency()
    insert_query_logger = Factory(AppLogger, name="InsertProductRecommendationQuery")
    get_query_logger = Factory(AppLogger, name="GetProductRecommendationQuery")
    repository_logger = Factory(AppLogger, name="ProductRecommendationRepository")
    service_logger = Factory(AppLogger, name="ProductRecommendationService")

    product_recommendation_mapper = Singleton(ProductRecommendationMapper)
    insert_product_recommendation_query = Singleton(
        InsertProductRecommendationQuery,
        session=mongo_session,
        logger=insert_query_logger,
    )
    get_product_recommendation_query = Singleton(
        GetProductRecommendationQuery, session=mongo_session, logger=get_query_logger
    )
    product_recommendation_repository = Factory(
        ProductRecommendationRepository,
        logger=repository_logger,
        product_recommendation_mapper=product_recommendation_mapper,
        get_product_recommendations_query_protocol=get_product_recommendation_query,
        insert_product_recommendations_query_protocol=insert_product_recommendation_query,
    )
    product_recommendation_service = Factory(
        ProductRecommendationService,
        product_recommendation_repository=product_recommendation_repository,
        logger=service_logger,
    )
