from typing import TYPE_CHECKING

from context.v1.emails.domain.entities.signin import SigninEmailEntity
from context.v1.emails.domain.steps.find import FindEmailStep
from context.v1.emails.domain.steps.verify_password import VerifyPasswordStep
from context.v1.login_methods.domain.steps.create_jwt import CreateJWTStep
from context.v1.login_methods.domain.steps.find import (
    FindLoginMethodStep,
)
from context.v1.refresh_token.domain.entities.refresh_token import (
    CreateRefreshTokenEntity,
)
from context.v1.refresh_token.domain.steps.create import CreateRefreshTokenStep
from shared.app.controllers.saga.controller import SagaController
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity


class SignInWithEmailUseCase:
    def __init__(
        self,
        user_repository: RepositoryInterface,
        email_repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
        refresh_token_repository: RepositoryInterface,
    ):
        self.user_repository = user_repository
        self.email_repository = email_repository
        self.login_method_repository = login_method_repository
        self.refresh_token_repository = refresh_token_repository

    def execute(self, payload: SigninEmailEntity):
        # Check if email
        # validate activation
        # validate password
        # generate JWT

        controller = SagaController(
            [
                FindEmailStep(email=payload.email, repository=self.email_repository),
                VerifyPasswordStep(password=payload.password),
                FindLoginMethodStep(
                    find_step_type=FindEmailStep,
                    repository=self.login_method_repository,
                ),
            ],
        )
        payloads = controller.execute()

        login_method: LoginMethodEntity = payloads[FindLoginMethodStep]

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
