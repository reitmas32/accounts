from fastapi import APIRouter, Request, status

from api.v1.codes.logic.schemas import ResentCodeSchema
from api.v1.codes.logic.services import CreateCodesService
from core.settings import log
from core.settings.database import use_database_session
from core.utils.responses import EnvelopeResponse

router = APIRouter(prefix="/codes", tags=["codes"])


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: ResentCodeSchema,
):
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a Code")
        return CreateCodesService(session=session).create(payload=payload)
