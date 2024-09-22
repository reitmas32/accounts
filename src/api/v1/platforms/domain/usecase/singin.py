from api.v1.login_methods.domain.steps.create_jwt import CreateJWTStep
from api.v1.login_methods.domain.steps.find import FindLoginMethodByPlatformStep
from api.v1.platforms.domain.entities.signin import SigninPlatformEntity
from api.v1.platforms.domain.steps.find import FindPlatformStep
from shared.app.controllers.saga.controller import SagaController
from shared.databases.infrastructure.repository import RepositoryInterface


class SignInPlatformUseCase:
    def __init__(
        self,
        repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
    ):
        self.repository = repository
        self.login_method_repository = login_method_repository

    def execute(self, payload: SigninPlatformEntity):

        controller = SagaController(
            [
                FindPlatformStep(external_id=payload.external_id, platform=payload.platform, repository=self.repository),
                FindLoginMethodByPlatformStep(repository=self.login_method_repository),
            ],
        )
        payloads = controller.execute()

        login_method: list= payloads[FindLoginMethodByPlatformStep][0]

        controller_jwt = SagaController(
            [CreateJWTStep(login_method=login_method)],
            prev_saga=controller,
        )

        payloads_jwt = controller_jwt.execute()

        return payloads_jwt[CreateJWTStep]
