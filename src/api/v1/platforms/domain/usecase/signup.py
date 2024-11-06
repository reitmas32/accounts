from context.v1.login_methods.domain.steps.create import CreateLoginMethodStep
from context.v1.login_methods.domain.steps.create_jwt import CreateJWTStep
from api.v1.platforms.domain.entities.platform import PlatformEntity
from api.v1.platforms.domain.entities.singup import SignupPlatformEntity
from api.v1.platforms.domain.steps.create import CreatePlatformStep
from api.v1.platforms.domain.steps.search import SearchPlatformStep
from api.v1.users.domain.steps.create import CreateUserByUserNameStep
from shared.app.controllers.saga.controller import SagaController
from shared.databases.infrastructure.repository import RepositoryInterface


class SignUpPlatformUseCase:
    def __init__(
        self,
        repository: RepositoryInterface,
        user_repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.login_method_repository = login_method_repository

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
                SearchPlatformStep(external_id=payload.external_id, platform=payload.platform, repository=self.repository),
                CreatePlatformStep(repository=self.repository, entity=platform),
                CreateLoginMethodStep(repository=self.login_method_repository),
            ],
        )
        payloads = controller.execute()

        controller_jwt = SagaController(
            [CreateJWTStep(login_method=payloads[CreateLoginMethodStep])],
            prev_saga=controller,
        )

        payloads_jwt = controller_jwt.execute()

        return payloads_jwt[CreateJWTStep]
