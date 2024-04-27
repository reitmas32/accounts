from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from api.v1.login_methods.filters import FilterLoginMethodSchema
from api.v1.login_methods.schemas import CreateLoginMethodSchema
from api.v1.login_methods.services import (
    CreateLoginMethodService,
    DeleteLoginMethodService,
    ListLoginMethodService,
    RetrieveLoginMethodService,
)
from core.settings import log
from core.settings.database import use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import (
    EnvelopeResponse,
    PaginationParams,
    default_pagination_params,
)

router = APIRouter(prefix="/login_methods", tags=["CRUD login methods"])


@router.get(
    "",
    summary="Lista todos los login methods",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def get_all(
    request: Request,
    pagination_params: PaginationParams = Depends(default_pagination_params),
    query_params: FilterLoginMethodSchema = Depends(),
    _=Depends(check_authorization),
) -> ListLoginMethodService:
    with use_database_session() as session:
        log.info("Get List of login methods")
        filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)
        return ListLoginMethodService(session=session).list(
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
) -> RetrieveLoginMethodService:
    with use_database_session() as session:
        log.info("Get only one Login Method")
        return RetrieveLoginMethodService(session=session).retrieve(id=id)


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateLoginMethodSchema,
    _=Depends(check_authorization),
):
    log.info("Create Login Method")
    with use_database_session() as session:
        return CreateLoginMethodService(session=session).create(payload=payload)


@router.delete(
    "/{id}",
    summary="elimina un login method",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def delte(
    id: UUID,
    _=Depends(check_authorization),
) -> RetrieveLoginMethodService:
    with use_database_session() as session:
        return DeleteLoginMethodService(session=session).delete(id=id)
