from typing import TYPE_CHECKING

from context.v1.emails.domain.steps.find import FindEmailStep
from shared.app.controllers.saga.controller import StepSAGA
from shared.app.errors.not_atorization import NotAuthorizedError
from shared.app.errors.saga import SAGAError
from shared.app.handlers.password import PasswordHandler

if TYPE_CHECKING:
    from context.v1.emails.domain.entities.email import EmailEntity


class VerifyPasswordStep(StepSAGA):
    def __init__(
        self,
        password: str,
    ):
        self.password = password

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        email: EmailEntity = all_payloads.get(FindEmailStep)
        if email is None:
            raise SAGAError("Run FindEmailStep before of VerifyPasswordStep")
        result = PasswordHandler.verify_password(
            plain_password=self.password, hashed_password=email.password
        )
        if not result:
            raise NotAuthorizedError(f"Password Invalid by email {email.email}")

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
