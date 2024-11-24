from typing import TYPE_CHECKING

from context.v1.login_methods.domain.steps.create_jwt import CreateJWTStep
from context.v1.login_methods.domain.steps.find import FindLoginMethodByPlatformStep
from context.v1.platforms.domain.entities.signin import SigninPlatformEntity
from context.v1.platforms.domain.steps.find import FindPlatformStep
from context.v1.refresh_token.domain.entities.refresh_token import (
    CreateRefreshTokenEntity,
)
from context.v1.refresh_token.domain.steps.create import CreateRefreshTokenStep
from shared.app.controllers.saga.controller import SagaController
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity


class SignInPlatformUseCase:
    def __init__(
        self,
        repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
        refresh_token_repository: RepositoryInterface,
    ):
        self.repository = repository
        self.login_method_repository = login_method_repository
        self.refresh_token_repository = refresh_token_repository

    def execute(self, payload: SigninPlatformEntity):
        controller = SagaController(
            [
                FindPlatformStep(
                    external_id=payload.external_id,
                    platform=payload.platform,
                    repository=self.repository,
                ),
                FindLoginMethodByPlatformStep(repository=self.login_method_repository),
            ],
        )
        payloads = controller.execute()

        login_method: LoginMethodEntity = payloads[FindLoginMethodByPlatformStep][0]

        controller_jwt = SagaController(
            [
                CreateJWTStep(login_method=login_method),
                CreateRefreshTokenStep(
                    repository=self.refresh_token_repository,
                    entity=CreateRefreshTokenEntity(
                        user_id=login_method.user_id,
                        login_method_id=login_method.id,
                    ),
                ),
            ],
            prev_saga=controller,
        )

        payloads_jwt = controller_jwt.execute()

        jwt = payloads_jwt[CreateJWTStep]

        refresh_token = payloads_jwt[CreateRefreshTokenStep]

        return jwt, refresh_token
