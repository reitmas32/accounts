from typing import TYPE_CHECKING

from context.v1.login_methods.domain.steps.create import CreateLoginMethodStep
from context.v1.login_methods.domain.steps.create_jwt import CreateJWTStep
from context.v1.platforms.domain.entities.platform import PlatformEntity
from context.v1.platforms.domain.entities.singup import SignupPlatformEntity
from context.v1.platforms.domain.steps.create import CreatePlatformStep
from context.v1.platforms.domain.steps.search import SearchPlatformStep
from context.v1.refresh_token.domain.entities.refresh_token import (
    CreateRefreshTokenEntity,
)
from context.v1.refresh_token.domain.steps.create import CreateRefreshTokenStep
from context.v1.users.domain.steps.create import CreateUserByUserNameStep
from shared.app.controllers.saga.controller import SagaController
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity
    from context.v1.users.domain.entities.user import UserEntity


class SignUpPlatformUseCase:
    def __init__(
        self,
        repository: RepositoryInterface,
        user_repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
        refresh_token_repository: RepositoryInterface,
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.login_method_repository = login_method_repository
        self.refresh_token_repository = refresh_token_repository

    def execute(self, payload: SignupPlatformEntity):
        # Crear el usuario
        # Validar el token
        # Crear el platform
        # Crear el login method

        platform = PlatformEntity(**payload.model_dump(), user_id=None)

        controller = SagaController(
            [
                CreateUserByUserNameStep(
                    user_name=payload.user_name, repository=self.user_repository
                ),
                # TODO: Validate the Token
                SearchPlatformStep(
                    external_id=payload.external_id,
                    platform=payload.platform,
                    repository=self.repository,
                ),
                CreatePlatformStep(repository=self.repository, entity=platform),
                CreateLoginMethodStep(repository=self.login_method_repository),
            ],
        )
        payloads = controller.execute()

        user_entity: UserEntity = payloads[CreateUserByUserNameStep]
        login_method_entity: LoginMethodEntity = payloads[CreateLoginMethodStep]

        controller_jwt = SagaController(
            [
                CreateJWTStep(login_method=payloads[CreateLoginMethodStep]),
                CreateRefreshTokenStep(
                    repository=self.refresh_token_repository,
                    entity=CreateRefreshTokenEntity(
                        user_id=user_entity.id,
                        login_method_id=login_method_entity.id,
                    ),
                ),
            ],
            prev_saga=controller,
        )

        payloads_jwt = controller_jwt.execute()

        jwt = payloads_jwt[CreateJWTStep]

        refresh_token = payloads_jwt[CreateRefreshTokenStep]

        return jwt, refresh_token
