from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from api.v1.emails.crud.filters import FilterEmailsSchema
from api.v1.emails.crud.schemas import CreateEmailSchema
from api.v1.emails.crud.services import (
    CreateEmailsService,
    DeleteEmailsService,
    ListEmailsService,
    RetrieveEmailsService,
)
from core.settings import log
from core.settings.database import use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import (
    EnvelopeResponse,
    PaginationParams,
    default_pagination_params,
)

router = APIRouter(prefix="/emails", tags=["CRUD emails"])


@router.get(
    "",
    summary="Lista todos los codes",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def get_all(
    request: Request,
    pagination_params: PaginationParams = Depends(default_pagination_params),
    query_params: FilterEmailsSchema = Depends(),
    _=Depends(check_authorization),
) -> ListEmailsService:
    with use_database_session() as session:
        log.info("Get List of Codes")
        filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)
        return ListEmailsService(session=session).list(
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
) -> RetrieveEmailsService:
    with use_database_session() as session:
        log.info("Get only one Service")
        return RetrieveEmailsService(session=session).retrieve(id=id)


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateEmailSchema,
    _=Depends(check_authorization),
):
    with use_database_session() as session:
        log.info("Create a Email")
        return CreateEmailsService(session=session).create(payload=payload)


@router.delete(
    "/{id}",
    summary="elimina un code",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def delte(
    id: UUID,
    _=Depends(check_authorization),
) -> RetrieveEmailsService:
    with use_database_session() as session:
        log.info("Get only one Service")
        return DeleteEmailsService(session=session).delete(id=id)
