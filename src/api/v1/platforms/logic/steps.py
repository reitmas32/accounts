from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from api.v1.platforms.crud.proxies import RepositoryPlatformUser
from api.v1.platforms.logic.schemas import SignupPlatformSchema
from api.v1.users.crud.proxies import RepositoryUser
from api.v1.users.crud.schemas import UserSchema
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import (
    PlatformSignUpUniqueException,
    UserNameUniqueException,
)
from core.utils.jwt import JWTHandler, TokenDataSchema

if TYPE_CHECKING:
    from models import UserModel
    from models.auth_general_platform import AuthGeneralPlatformModel


class CreateUserStep(StepSAGA):
    """
    Step in the SAGA process for creating a user.

    This step handles the creation of a user account during the signup process.

    Args:
        user (SignupEmailSchema): Data schema containing user signup information.
        session: Database session for interacting with the data.

    Attributes:
        user_created: User object created during the step.
        user (SignupEmailSchema): Data schema containing user signup information.
        repository: Repository for user data operations.
    """

    def __init__(self, user: UserSchema, session: Session):  # TODO: Change SignupEmailSchema to UserSchema
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_created = None
        self.user = user
        self.repository = RepositoryUser(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        existing_user_name = self.repository.get_user(user_name=self.user.user_name)
        if existing_user_name is not None:
            raise UserNameUniqueException(user_name=self.user.user_name)

        self.user_created: UserModel = self.repository.add(
            user_name=self.user.user_name,
            birthday=self.user.birthday,
            name=self.user.name,
        )

        if self.user_created is None:
            raise UserNameUniqueException(user_name=self.user.user_name)

        return self.user_created

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        if self.user_created is not None:
            self.repository.delete_by_id(self.user_created.id)


class CreatePlatformUserStep(StepSAGA):
    """
    Step in the SAGA process for creating a user.

    This step handles the creation of a user account during the signup process.

    Args:
        user (SignupEmailSchema): Data schema containing user signup information.
        session: Database session for interacting with the data.

    Attributes:
        user_created: User object created during the step.
        user (SignupEmailSchema): Data schema containing user signup information.
        repository: Repository for user data operations.
    """

    def __init__(self, user: SignupPlatformSchema, session: Session):  # TODO: Change SignupEmailSchema to UserSchema
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_created = None
        self.user = user
        self.repository: RepositoryPlatformUser = RepositoryPlatformUser(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        existing_platform_user = self.repository.exists_id_of_platform(
            hashed_platform_id=self.user.id_user,
            platform=self.user.platform,
            user_id=payload.id,
        )
        if existing_platform_user:
            raise PlatformSignUpUniqueException(platform=self.user.platform)

        self.platform_user_created: AuthGeneralPlatformModel = self.repository.add(
            user_id=payload.id,
            hashed_platform_id=self.user.id_user,
            type=self.user.platform,
            active=False,
        )

        return JWTHandler.create_token(TokenDataSchema(user_id=self.platform_user_created.user_id.__str__()))

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        if self.platform_user_created is not None:
            self.repository.delete_by_id(self.platform_user_created.id)
