from fastapi import (
    APIRouter,
    Depends,
    status,
    Request
)
from sqlalchemy.orm import Session
from api.v1.users.schemas import (
    CreateUserSchema,
    ActivateAccountUserSchema,
    LoginUserSchema,
    ValidateTokenSchema
)
from api.v1.users.services import (
    CreateUserService,
    RetrieveUserService,
    ListUserService,
    ActivateAccountService,
    LoginUserService,
    ResourcesServices
)
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)
from core.settings.database import get_session
from pydantic import EmailStr
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def create(
    request: Request,
    payload: CreateUserSchema,
    session: Session = Depends(get_session)
):

    log.info("Create User")
    return CreateUserService(session=session).create(payload=payload)


@router.get(
    "/{id}",
    summary="Regresa los datos de un usuario en especifico a partir de su id", 
    status_code=status.HTTP_200_OK, 
    response_model=EnvelopeResponse
)
async def retrieve(
    request: Request,
    id : UUID,
    session: Session = Depends(get_session),
):
    log.info("Get User")
    return RetrieveUserService(session=session).retrieve_by_id(id=id)

@router.get(
    "",
    summary="Listar todos los usuarios", 
    status_code=status.HTTP_200_OK, 
    response_model=EnvelopeResponse
)
async def get_all(
    request: Request,
    session: Session = Depends(get_session),
):

    log.info("Get List Users")
    return ListUserService(session=session).list()


@router.post(
    "/activate-account",
    summary="Activar cuenta de usuario",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse
)
async def activate_account(
    request: Request,
    payload: ActivateAccountUserSchema,
    session: Session = Depends(get_session),
):
    
    log.info("Activar cuenta de usuario")
    return ActivateAccountService(session=session).activate_account(payload=payload)



@router.post(
    "/login",
    summary="Login de cuenta de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse
)
async def login(
    request: Request,
    payload: LoginUserSchema,
    session: Session = Depends(get_session),
):
    
    log.info("Login usuario")
    return LoginUserService(session=session).login(payload=payload)


@router.post(
    "/validate-token",
    summary="Valida el token y te regresa la data inmersa en el",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse
)
async def validate_token(
    request: Request,
    payload: ValidateTokenSchema,
    session: Session = Depends(get_session),
):
    
    log.info("Validando token de usuario")
    return LoginUserService(session=session).validate_token(payload=payload)


@router.get(
    "/resources/public-key",
    summary="Te regresa la llave publica con la cual podras validar los token de los usuarios", 
    status_code=status.HTTP_200_OK, 
    response_model=EnvelopeResponse
)
async def get_public_key(
    request: Request
):

    log.info("Get Public Key")
    return ResourcesServices.get_public_key()


@router.get(
    "/resources/2FA",
    summary="Te regresa la lista de servicios disponibles con los cuales el usuario podra activar el doble factor de autenticacion", 
    status_code=status.HTTP_200_OK, 
    response_model=EnvelopeResponse
)
async def get_list_2FA_available_system(
    request: Request
):

    log.info("Get all available 2FA system")
    return ResourcesServices.get_list_2FA_available_system()


@router.get(
    "/resources/activation_methods",
    summary="Te regresa la lista de servicios disponibles con los cuales el usuario podra crear una cuenta de usuario y hacer login", 
    status_code=status.HTTP_200_OK, 
    response_model=EnvelopeResponse
)
async def get_list_activation_methods_available_system(
    request: Request
):

    log.info("Get all available activation methods")
    return ResourcesServices.get_list_activation_methods_available_system()