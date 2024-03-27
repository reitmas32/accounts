from api.v1.users.schemas import (
    CreateUserSchema,
    RetrieveUserServiceSchema,
    ListUserSchema,
    ActivateAccountUserSchema,
    LoginUserSchema,
    ValidateTokenSchema
)
from api.v1.users.proxies import RepositoryUser
from core.utils.responses import create_envelope_response
import logging
from api.v1.users.utils import CodeManager
from models.enum import CodeTypeEnum, UserActivationMethodEnum
from core.utils.exceptions import FormException
from uuid import UUID
from core.utils.email import SendEmailAbstract
from core.utils.email import SendEmailAbstract, get_current_manager_email_to_app_standard
from api.v1.users.resources import get_data_for_email_activation_success
from models.enum import UserAuthMethodEnum,UserActivationMethodEnum
from core.utils.password import PasswordManager
from core.utils.jwt import JWTHandler,TokenDataSchema
from core.settings import settings


logger = logging.getLogger(__name__)


class ListUserService():
    def __init__(self,session):
        self.session = session
        self.repository_user = RepositoryUser(
            session = session 
        )
        
    def list(self):
        all_users = self.repository_user.get_by_attributes(
            is_removed = False
        )
        data = [ListUserSchema(**user.as_dict()) for user in all_users]
        count = len(data)
        return create_envelope_response(data=data, count=count)


class RetrieveUserService():
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
            data = RetrieveUserServiceSchema(**user.as_dict())
            count = 1
        return create_envelope_response(data=data, count=count)


class CreateUserService():

    def __init__(self,session):
        self.session = session
        self.repository_user = RepositoryUser(
            session = session 
        )
        self.code_manager = CodeManager(
            session = session
        )
        
    def create(self,payload:CreateUserSchema):
        exist_user = self.repository_user.exists_email_or_user_name(
            email=payload.email,
            user_name=payload.user_name
        )
        if exist_user:
            raise FormException(
                field_errors={
                    'general': "Already exist register user with the same email or same user_name"
                }
            )
        user_created = self.repository_user.add(
            password=PasswordManager.hash_password(password=payload.password), 
            **payload.model_dump(exclude={"password"})
        )
        user_schema = RetrieveUserServiceSchema(**user_created.as_dict())
        if user_created:
            self.code_manager.create_and_send_code(
                user_name=user_created.user_name,
                email=user_created.email,
                code_type=CodeTypeEnum.ACCOUNT_ACTIVATION
            )
        return create_envelope_response(data=user_schema)



class ActivateAccountService():
    def __init__(self,session):
        self.session = session
        self.repository_user = RepositoryUser(
            session = session 
        )
        self.code_manager = CodeManager(
            session = session
        )
        self.manager_email : SendEmailAbstract = get_current_manager_email_to_app_standard()

    
    def activate_account(self,payload:ActivateAccountUserSchema):
        user = self.repository_user.get_last_user_with_specifi_email(
            email=payload.email
        )
        if not user:
            raise FormException(
                field_errors={
                    'email': "Don't exist any register with this email"
                }
            )
        if user.validate:
          raise FormException(
                field_errors={
                    'detail': "The user has been activated"
                }
            )
        code_valid = self.code_manager.validate_code(
            email=payload.email,
            code=payload.code,
            code_type=CodeTypeEnum.ACCOUNT_ACTIVATION
        )
        if code_valid:
            user.validate = True
            user.activation_method = UserActivationMethodEnum.EMAIL
            self.session.commit()
            data = "The user account has been successfully activated. The user can now log in."
            subject_text, body_text = get_data_for_email_activation_success(
                user_name = user.user_name
            )
            self.manager_email.send_email(
                email_subject = user.email,
                subject_text = subject_text,
                message_text = body_text
            )
        else:
            raise FormException(
                field_errors={
                    'code': "The activation code is invalid or has expired"
                }
            )
        return create_envelope_response(data=data)
    

class LoginUserService():
    def __init__(self,session):
        self.session = session
        self.repository_user = RepositoryUser(
            session = session 
        )
        
    def login(self,payload:LoginUserSchema):
        user = self.repository_user.get_user(
            email=payload.email
        )
        if not user:
            raise FormException(
                field_errors={
                    'email': "Don't exist any register with this email or the user account is not activate"
                }
            )
        is_valid_password = PasswordManager.verify_password(
            plain_password = payload.password,
            hashed_password = user.password
        )
        if not is_valid_password:
            raise FormException(
                field_errors={
                    'password': "Password incorrect"
                }
            )
        response = {
            'token_user_login' : JWTHandler.create_token(
                data = TokenDataSchema(user_mother_id=str(user.id))
            )
        }
        return create_envelope_response(data=response)

    def validate_token(self,payload:ValidateTokenSchema):
        try:
            response = JWTHandler.validate_token(
                    token=payload.token
                )
        except Exception as e:
            raise FormException(
                field_errors={
                    'token': "The activation code is invalid or has expired"
                }
            )            
        return create_envelope_response(data=response.model_dump())
    

class ResourcesServices():

    @staticmethod
    def get_public_key():
        return create_envelope_response(
            data={
                'public_key' : settings.PRIVATE_KEY_JWT
            }
        )
    
    @staticmethod
    def get_list_2FA_available_system():
        list_2FA_available = UserAuthMethodEnum.list_values()
        count = len(list_2FA_available)
        return create_envelope_response(
            data = list_2FA_available,
            count=count
        )    

    @staticmethod
    def get_list_activation_methods_available_system():
        list_activation_methods = UserActivationMethodEnum.list_values()
        count = len(list_activation_methods)
        return create_envelope_response(
            data = list_activation_methods,
            count=count
        )    

