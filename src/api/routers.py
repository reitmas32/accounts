from fastapi import APIRouter

from api.health.endpoints import router as healthcheck_endpoints
from api.v1.codes.presentation.endpoints import router as codes_endpoints
from api.v1.emails.presentation.endpoints import router as emails_endpoints
from api.v1.login_methods.presentation.endpoints import (
    router as login_methods_endpoints,
)
from api.v1.platforms.presentation.endpoints import router as platforms_endpoints
from api.v1.users.presentation.endpoints import router as users_endpoints
from core.settings import settings

api_healthcheck_router = APIRouter()
api_healthcheck_router.include_router(healthcheck_endpoints)

api_v1_router = APIRouter(prefix=f"/api/{settings.API_V1}")
api_v1_router.include_router(codes_endpoints)
api_v1_router.include_router(emails_endpoints)
api_v1_router.include_router(login_methods_endpoints)
api_v1_router.include_router(platforms_endpoints)
api_v1_router.include_router(users_endpoints)


