from context.v1.emails.domain.entities.email import EmailEntity
from context.v1.users.domain.entities.user import UserEntity
from shared.app.controllers.saga.controller import StepSAGA
from shared.app.errors.invalid.type_invalid import TypeInvalidError
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateEmailStep(StepSAGA):
    def __init__(self, entity: EmailEntity, repository: RepositoryInterface):
        self.entity = entity
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        self.email = None
        if type(payload) is not UserEntity:
            raise TypeInvalidError(valid_type=UserEntity, invalid_type=type(payload))
        self.entity.user_id = payload.id

        self.email = self.repository.add(**self.entity.model_dump())
        return self.email

    def rollback(self):
        """
        Rollback the step, deleting the email account if it was created.
        """
        if self.email is not None:
            self.repository.delete_by_id(self.email.id)
