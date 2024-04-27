from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from api.v1.codes.crud.filters import FilterCodesSchema
from api.v1.codes.crud.schemas import CreateCodeSchema
from api.v1.codes.crud.services import (
    CreateCodesService,
    DeleteCodesService,
    ListCodesService,
    RetrieveCodesService,
)
from core.settings import log
from core.settings.database import use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import (
    EnvelopeResponse,
    PaginationParams,
    default_pagination_params,
)

router = APIRouter(prefix="/codes", tags=["CRUD codes"])


@router.get(
    "",
    summary="Lista todos los codes",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def get_all(
    request: Request,
    pagination_params: PaginationParams = Depends(default_pagination_params),
    query_params: FilterCodesSchema = Depends(),
    _=Depends(check_authorization),
) -> ListCodesService:
    with use_database_session() as session:
        log.info("Get List of Codes")
        filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)
        return ListCodesService(session=session).list(
            filters=filters, pagination_params=pagination_params, request=request
        )


@router.get(
    "/{id}",
    summary="Obtiene un Service especifico",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve(
    id: UUID,
    _=Depends(check_authorization),
) -> RetrieveCodesService:
    with use_database_session() as session:
        log.info("Get only one Service")
        return RetrieveCodesService(session=session).retrieve(id=id)


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateCodeSchema,
    _=Depends(check_authorization),
):
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return CreateCodesService(session=session).create(payload=payload)


@router.delete(
    "/{id}",
    summary="elimina un code",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def delte(
    id: UUID,
    _=Depends(check_authorization),
) -> RetrieveCodesService:
    with use_database_session() as session:
        log.info("Get only one Service")
        return DeleteCodesService(session=session).delete(id=id)
