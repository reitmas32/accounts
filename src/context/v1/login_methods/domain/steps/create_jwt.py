from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from shared.app.controllers.saga.controller import StepSAGA
from shared.app.handlers.jwt import JWTHandler
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.presentation.schemas.jwt import JWTSchema


class CreateJWTStep(StepSAGA):
    def __init__(self, login_method: LoginMethodEntity):
        self.login_method = login_method

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        if self.login_method is None:
            raise EntityNotFoundError(resource="login_method")
        return JWTHandler.create_token(JWTSchema(**self.login_method.model_dump(mode="json")))

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
