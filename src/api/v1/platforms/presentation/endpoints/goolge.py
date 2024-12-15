
import requests
from fastapi import status
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api.v1.platforms.presentation.endpoints.routers import router_operations as router
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.platforms.domain.entities.singup import SignupPlatformEntity
from context.v1.platforms.domain.usecase.signup import SignUpPlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.settings import settings
from core.settings.database import get_session
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity


# Rutas para el flujo de autenticación
@router.get("/google/login")
async def login():
    """
    Redirige al usuario a la página de login de Google.
    """
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code"
        f"&client_id={settings.CLIENT_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        f"&scope={settings.SCOPES}"
    )
    return RedirectResponse(url=google_auth_url)


@router.get(
    "/google/callback",
    summary="Signup By Platform",
    status_code=status.HTTP_201_CREATED,
)
async def auth_callback(code: str, session: Session = Depends(get_session)):
    # Procesar el código y obtener el token y los datos del usuario
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code != 200:
        return {"error": "Failed to fetch token"}, 400

    token_info = token_response.json()
    access_token = token_info.get("access_token")

    # Hasta aca podemos meternos

    # Obtener información del usuario
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_info_response.status_code != 200:
        return {"error": "Failed to fetch user info"}, 400

    user_info = user_info_response.json()

    # Extraer información del usuario
    user_id = user_info.get("id")

    body = {
        "external_id": user_id,
        "platform": "google",
        "token": access_token,
    }

    entity: SignupPlatformEntity = SignupPlatformEntity(**body)

    use_case = SignUpPlatformUseCase(
        repository=PlatformRepository(session=session),
        user_repository=UserRepository(session=session),
        login_method_repository=LoginMethodRepository(session=session),
        refresh_token_repository=RefreshTokenRepository(session=session),
    )

    jwt, refresh_token = use_case.execute(payload=entity)

    return ResponseEntity(
        data={"jwt": jwt, "refresh_token": refresh_token},
        code=StatusCodes.HTTP_201_CREATED,
    )
