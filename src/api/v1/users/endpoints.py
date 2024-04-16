from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.users.schemas import SignupEmailSchema, VerifyEmailSchema
from api.v1.users.services import (
    RetrieveUserService,
    SignUpEmailService,
)
from api.v1.users.services.verify import VerifyCodeService
from core.settings import log
from core.settings.database import get_session, use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import (
    EnvelopeResponse,
)

router = APIRouter(prefix="/users")


@router.get(
    "/",
    summary="Returns a list of users",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["users"],
)
async def retrieve_all(
    request: Request,
    _=Depends(check_authorization),
    session: Session = Depends(get_session),
):
    """
    Retrieve all users.

    This endpoint retrieves information for all users in the database.

    Args:
        request (Request): FastAPI request object.
        _: Dependency to check authorization (ignored).
        session (Session): Database session for interacting with the data.

    Returns:
        dict: Envelope response containing user data, count, message, and status code.
    """
    log.info("Get User")
    return RetrieveUserService(session=session).retrieve_all()


@router.get(
    "/{user_id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["users"],
)
async def retrieve_one(
    request: Request,
    user_id: UUID,
    _=Depends(check_authorization),
    session: Session = Depends(get_session),
):
    """
    Retrieve data of the authenticated user.

    This endpoint retrieves information of the authenticated user by user ID.

    Args:
        request (Request): FastAPI request object.
        user_id (UUID): ID of the user to retrieve.
        _: Dependency to check authorization (ignored).
        session (Session): Database session for interacting with the data.

    Returns:
        dict: Envelope response containing user data, count, message, and status code.
    """
    log.info("Get User")
    return RetrieveUserService(session=session).retrieve_by_id(id=user_id)


@router.post(
    "/email/signup",
    summary="Create user registration via email",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_signup(
    request: Request,
    payload: SignupEmailSchema,
    _=Depends(check_authorization),
):
    """
    Create a user registration via email.

    This endpoint allows the creation of a user account using email as the authentication method.

    Args:
        request (Request): FastAPI request object.
        payload (SignupEmailSchema): Data payload containing email signup information.
        _: Dependency to check authorization (ignored).

    Returns:
        dict: Envelope response containing user data, message, and status code.
    """
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return SignUpEmailService(session=session).create(payload=payload)


@router.put(
    "/email/verify",
    summary="Verifica un email enviando un correo con un codigo",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_verify(
    request: Request,
    payload: VerifyEmailSchema,
    _=Depends(check_authorization),
):
    """
    Create a user registration via email.\n

    This endpoint allows the creation of a user account using email as the authentication method.

    Args:
        request (Request): FastAPI request object.\n
        payload (SignupEmailSchema): Data payload containing email signup information.\n
        _: Dependency to check authorization (ignored).\n

    Returns:
        dict: Envelope response containing user data, message, and status code\n.
    """
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return VerifyCodeService(session=session).verify(payload=payload)


"""
@router.patch(
    "/email/login",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_login(
    request: Request,
    payload: SignupEmailSchema,
    _=Depends(check_authorization),
):
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return CreateUserService(session=session).create_by_email(payload=payload)


@router.post(
    "/email/activation",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_activation(
    request: Request,
    payload: SignupEmailSchema,
    _=Depends(check_authorization),
):
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
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
    "/login",
    summary="Login de cuenta de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
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
"""
