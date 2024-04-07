from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from api.v1.services.filters import FilterServicesSchema
from api.v1.services.schemas import CreateServiceSchema
from api.v1.services.service import (
    CreateServicesService,
    ListServicesService,
    RetrieveServicesService,
)
from core.settings import log
from core.settings.database import use_database_session
from core.utils.autorization import check_autorization
from core.utils.responses import (
    EnvelopeResponse,
    PaginationParams,
    default_pagination_params,
)

router = APIRouter(prefix="/services", tags=["services"])


@router.get(
    "",
    summary="Lista todos los periodos de desembolso",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def get_all(
    request: Request,
    pagination_params: PaginationParams = Depends(default_pagination_params),
    query_params: FilterServicesSchema = Depends(),
    _=Depends(check_autorization),
) -> ListServicesService:
    with use_database_session() as session:
        log.info("Get List of Services")
        filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)
        return ListServicesService(session=session).list(
            filters=filters, pagination_params=pagination_params, request=request
        )


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateServiceSchema,
    _=Depends(check_autorization),
):
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return CreateServicesService(session=session).create(payload=payload)


@router.get(
    "/{id}",
    summary="Obtiene un Service especifico",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve(
    id: UUID,
    _=Depends(check_autorization),
) -> RetrieveServicesService:
    with use_database_session() as session:
        log.info("Get only one Service")
        return RetrieveServicesService(session=session).retrieve(id=id)
