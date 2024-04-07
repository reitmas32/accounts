from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.common.dependencies import get_data_token
from api.v1.users.schemas import (
    ActivateAccountUserSchema,
    CreateUserAuthEmailSchema,
    CreateUserAuthPlatformSchema,
    LoginAuthEmailSchema,
    LoginAuthGeneralPlatformSchema,
)
from api.v1.users.services import (
    ActivateAccountService,
    CreateUserService,
    LoginUserService,
    ResourcesServices,
    RetrieveUserService,
)
from core.settings import log
from core.settings.database import get_session
from core.utils.jwt import TokenDataSchema
from core.utils.responses import (
    EnvelopeResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    summary="Regresa los datos del usuario autenticado",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve(
    request: Request,
    token_payload: TokenDataSchema = Depends(get_data_token),
    session: Session = Depends(get_session),
):
    log.info("Get User")
    return RetrieveUserService(session=session).retrieve_by_id(id=token_payload.user_mother_id)


@router.post(
    "", summary="Crear registro de usuario", status_code=status.HTTP_201_CREATED, response_model=EnvelopeResponse
)
async def create(request: Request, payload: CreateUserAuthEmailSchema, session: Session = Depends(get_session)):
    log.info("Create User")
    return CreateUserService(session=session).create_by_email(payload=payload)


@router.post(
    "/activate-account",
    summary="Activar cuenta de usuario",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def activate_account(
    request: Request,
    payload: ActivateAccountUserSchema,
    session: Session = Depends(get_session),
):
    log.info("Activar cuenta de usuario")
    return ActivateAccountService(session=session).activate_account(payload=payload)


@router.post(
    "/login", summary="Login de cuenta de usuario", status_code=status.HTTP_201_CREATED, response_model=EnvelopeResponse
)
async def login(
    request: Request,
    payload: LoginAuthEmailSchema,
    session: Session = Depends(get_session),
):
    log.info("Login usuario")
    return LoginUserService(session=session).login_by_email(payload=payload)


@router.get(
    "/resources/public-key",
    summary="Te regresa la llave publica con la cual podras validar los token de los usuarios",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def get_public_key(request: Request):
    log.info("Get Public Key")
    return ResourcesServices.get_public_key()


@router.get(
    "/resources/activation_methods",
    summary="Te regresa la lista de servicios disponibles con los cuales el usuario podra crear una cuenta de usuario y hacer login",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def get_list_activation_methods_available_system(request: Request):
    log.info("Get all available activation methods")
    return ResourcesServices.get_list_activation_methods_available_system()


@router.post(
    "/platform/signup",
    summary="Crear un registro de usuario a traves de una plataforma",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create_by_platform(
    request: Request,
    payload: CreateUserAuthPlatformSchema,
    session: Session = Depends(get_session),
):
    log.info("Create User")
    return CreateUserService(session=session).create_by_platform(payload=payload)


@router.post(
    "/platform/login",
    summary="Login de cuenta de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def login_by_platform(
    request: Request,
    payload: LoginAuthGeneralPlatformSchema,
    session: Session = Depends(get_session),
):
    log.info("Login usuario")
    return LoginUserService(session=session).login_by_platform(payload=payload)
