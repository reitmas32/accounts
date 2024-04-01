import logging
from uuid import UUID

from api.v1.users.proxies import (
    RepositoryAuthEmail,
    RepositoryAuthGeneralPlatform,
    RepositoryUser,
    RepositoryUserLoginMethod,
)
from api.v1.users.resources import get_data_for_email_activation_success
from api.v1.users.schemas import (
    ActivateAccountUserSchema,
    CreateUserAuthEmailSchema,
    CreateUserAuthPlatformSchema,
    LoginAuthEmailSchema,
    LoginAuthGeneralPlatformSchema,
    ResponseCreateUserAuthEmailSchema,
    RetrieveUserSchema,
    ValidateTokenSchema,
)
from api.v1.users.utils import CodeManager
from core.settings import settings
from core.utils.email import (
    SendEmailAbstract,
    get_current_manager_email_to_app_standard,
)
from core.utils.exceptions import FormException
from core.utils.jwt import JWTHandler, TokenDataSchema
from core.utils.password import PasswordManager
from core.utils.platform import PlatformIDHasher
from core.utils.responses import create_envelope_response
from models.enum import CodeTypeEnum, UserActivationMethodEnum, UserLoginMethodsTypeEnum

logger = logging.getLogger(__name__)


class RetrieveUserService:
    def __init__(self,session):
        self.session = session
        self.repository_user = RepositoryUser(
            session = session
        )
    def retrieve_by_id(self,id:UUID):
        user = self.repository_user.get_by_id(
            id = id
        )
        data=None
        count=0
        if user:
            data = RetrieveUserSchema(**user.as_dict())
            count = 1
        return create_envelope_response(data=data, count=count)


class CreateUserService:

    def __init__(self,session):
        self.session = session
        self.repository_user = RepositoryUser(
            session = session
        )
        self.repository_auth_email = RepositoryAuthEmail(
            session = session
        )
        self.repository_login_method = RepositoryUserLoginMethod(
            session=session
        )
        self.repository_auth_platform = RepositoryAuthGeneralPlatform(
            session = session
        )
        self.repository_auth_email
        self.code_manager = CodeManager(
            session = session
        )

    def create_by_platform(self,payload:CreateUserAuthPlatformSchema):
        auth_platform = None
        user_with_user_name = None
        user_with_user_name = self.repository_user.get_user(user_name=payload.user_name)
        if not user_with_user_name:
            auth_platform = self.repository_auth_platform.get_auth_platform(
                hashed_platform_id =PlatformIDHasher.hash_hashed_platform_id(
                    hashed_platform_id=payload.platform_id
                ),
                type=payload.type
            )
        if user_with_user_name or auth_platform:
            raise FormException(
                field_errors={
                    "general": "Already exist register user with the same platform or same user_name"
                }
            )
        user_created = self.repository_user.add(
            user_name = payload.user_name,
            phone_number = payload.phone_number,
            extra_data = payload.extra_data
        )
        auth_platform_created = self.repository_auth_platform.add(
            user_id = user_created.id,
            email = payload.email,
            hashed_platform_id = PlatformIDHasher.hash_hashed_platform_id(payload.platform_id),
            active = True,
            type = payload.type
        )
        self.repository_login_method.add(
            user_id = user_created.id,
            entity_id = auth_platform_created.id,
            entity_type = UserLoginMethodsTypeEnum.AUTH_GENERAL_PLATFORMS
        )
        user_schema = RetrieveUserSchema(**user_created.as_dict())
        response = ResponseCreateUserAuthEmailSchema(
            user = user_schema,
            token = JWTHandler.create_token(
                data = TokenDataSchema(user_mother_id=str(auth_platform_created.user_id))
            )
        )
        return create_envelope_response(data=response)

    def create_by_email(self,payload:CreateUserAuthEmailSchema):
        auth_email = None
        user_with_user_name = None
        user_with_user_name = self.repository_user.get_user(user_name=payload.user_name)
        if not user_with_user_name:
            auth_email = self.repository_auth_email.get_auth_email(
                email=payload.email,
            )
        if user_with_user_name or auth_email:
            raise FormException(
                field_errors={
                    "general": "Already exist register user with the same email or same user_name"
                }
            )
        user_created = self.repository_user.add(
            user_name = payload.user_name,
            phone_number = payload.phone_number,
            extra_data = payload.extra_data
        )
        auth_email_created = self.repository_auth_email.add(
            user_id = user_created.id,
            email = payload.email,
            password = PasswordManager.hash_password(password=payload.password),
            active = False
        )
        self.repository_login_method.add(
            user_id = user_created.id,
            entity_id = auth_email_created.id,
            entity_type = UserLoginMethodsTypeEnum.AUTH_EMAIL
        )
        user_schema = RetrieveUserSchema(**user_created.as_dict())
        if user_created:
            self.code_manager.create_and_send_code(
                user_name=payload.user_name,
                email=payload.email,
                code_type=CodeTypeEnum.ACCOUNT_ACTIVATION
            )
        return create_envelope_response(data=user_schema)


class ActivateAccountService:
    def __init__(self,session):
        self.session = session
        self.repository_auth_email = RepositoryAuthEmail(
            session = session
        )
        self.code_manager = CodeManager(
            session = session
        )
        self.manager_email : SendEmailAbstract = get_current_manager_email_to_app_standard()
    def activate_account(self,payload:ActivateAccountUserSchema):
        auth_email = self.repository_auth_email.get_auth_email(
            email=payload.email
        )
        if not auth_email:
            raise FormException(
                field_errors={
                    "email": "Don't exist any register with this email"
                }
            )
        if auth_email.active:
          raise FormException(
                field_errors={
                    "detail": "The user has been activated"
                }
            )
        code_valid = self.code_manager.validate_code(
            email=payload.email,
            code=payload.code,
            code_type=CodeTypeEnum.ACCOUNT_ACTIVATION
        )
        if code_valid:
            auth_email.active = True
            self.session.commit()
            data = "The user account has been successfully activated.The user can now log in."
            subject_text, body_text = get_data_for_email_activation_success(
                user_name = auth_email.user.user_name
            )
            self.manager_email.send_email(
                email_subject = auth_email.email,
                subject_text = subject_text,
                message_text = body_text
            )
        else:
            raise FormException(
                field_errors={
                    "code": "The activation code is invalid or has expired"
                }
            )
        return create_envelope_response(data=data)


class LoginUserService:
    def __init__(self,session):
        self.session = session
        self.repository_auth_email = RepositoryAuthEmail(
            session = session
        )
        self.repository_auth_platform = RepositoryAuthGeneralPlatform(
            session = session
        )

    def login_by_platform(self,payload:LoginAuthGeneralPlatformSchema):
        auth_platform = self.repository_auth_platform.get_auth_platform(
            hashed_platform_id  = PlatformIDHasher.hash_hashed_platform_id (payload.platform_id ),
            type = payload.type
        )
        if not auth_platform:
            raise FormException(
                field_errors={
                    "general": "Don't exist any register with this hashed_platform_id  and type"
                }
            )
        response = {
            "token" : JWTHandler.create_token(
                data = TokenDataSchema(user_mother_id=str(auth_platform.user_id))
            )
        }
        return create_envelope_response(data=response)

    def login_by_email(self,payload:LoginAuthEmailSchema):
        auth_email = self.repository_auth_email.get_auth_email(
            email=payload.email
        )
        if not auth_email:
            raise FormException(
                field_errors={
                    "email": "Don't exist any register with this email or the user account is not activate"
                }
            )
        elif not auth_email.active:
            raise FormException(
                field_errors={
                    "general": "Your account is not active, you need active"
                }
            )
        is_valid_password = PasswordManager.verify_password(
            plain_password = payload.password,
            hashed_password = auth_email.password
        )
        if not is_valid_password:
            raise FormException(
                field_errors={
                    "password": "Password incorrect"
                }
            )
        response = {
            "token" : JWTHandler.create_token(
                data = TokenDataSchema(user_mother_id=str(auth_email.user_id))
            )
        }
        return create_envelope_response(data=response)
    def validate_token(self,payload:ValidateTokenSchema):
        try:
            response = JWTHandler.validate_token(
                    token=payload.token
                )
        except Exception:
            raise FormException(
                field_errors={
                    "token": "The activation code is invalid or has expired"
                }
            )
        return create_envelope_response(data=response.model_dump())


class ResourcesServices:
    @staticmethod
    def get_public_key():
        return create_envelope_response(
            data={
                "public_key" : settings.PRIVATE_KEY_JWT
            }
        )
    @staticmethod
    def get_list_activation_methods_available_system():
        list_activation_methods = UserActivationMethodEnum.list_values()
        count = len(list_activation_methods)
        return create_envelope_response(
            data = list_activation_methods,
            count=count
        )

