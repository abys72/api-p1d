from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory, Singleton

from app.modules.v1.endpoints.auth.access_token.login_user_service import LoginUserService
from app.modules.v1.endpoints.auth.access_token.query.login_user_query import LoginUserQuery
from app.modules.v1.endpoints.auth.access_token.repository.login_user_repository import LoginUserRepository
from app.shared.utils.logger import AppLogger


class LoginUserContainer(DeclarativeContainer):
    mongo_session = Dependency()
    login_user_query_logger = Factory(AppLogger, name="LoginUserQuery")
    repository_logger = Factory(AppLogger, name="LoginUserRepository")
    service_logger = Factory(AppLogger, name="LoginUserService")

    login_user_query = Singleton(LoginUserQuery, session=mongo_session,
                                 logger=login_user_query_logger)
    login_user_repository = Factory(LoginUserRepository,
                                    logger=repository_logger,
                                    login_user_query=login_user_query)
    login_user_service = Factory(LoginUserService,
                                 user_repository=login_user_repository,
                                 logger=service_logger
                                 )
