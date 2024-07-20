from fastapi import APIRouter

from api.health.endpoints import router as healthcheck_endpoints
from api.v1.codes.crud.endpoints import router as codes_crud_endpoints
from api.v1.emails.crud.endpoints import router as emails_crud_endpoints
from api.v1.emails.logic.endpoints import router as emails_logic_endpoints
from api.v1.login_methods.endpoints import router as login_methods_crud_endpoints
from api.v1.platforms.logic.endpoints import router as platform_logic_endpoints
from api.v1.users.crud.endpoints import router as users_crud_endpoints
from core.settings import settings

api_healthcheck_router = APIRouter()
api_healthcheck_router.include_router(healthcheck_endpoints)

api_v1_router = APIRouter(prefix=f"/api/{settings.API_V1}")
api_v1_router.include_router(users_crud_endpoints)
api_v1_router.include_router(codes_crud_endpoints)
api_v1_router.include_router(emails_crud_endpoints)
api_v1_router.include_router(login_methods_crud_endpoints)
api_v1_router.include_router(emails_logic_endpoints)
api_v1_router.include_router(platform_logic_endpoints)
