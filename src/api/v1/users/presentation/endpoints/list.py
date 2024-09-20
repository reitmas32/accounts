
from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from core.settings import log
from core.settings.database import get_session
from core.utils.responses import (
    EnvelopeResponse,
    EnvelopeResponseBody,
)

from .routers import router


@router.get(
    "/",
    summary="Returns a list of users",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    session: Session = Depends(get_session),
):
    log.info("Get All Users")
    body = EnvelopeResponseBody(links=None, count=0, results=[]).model_dump()
    return EnvelopeResponse(
        errors=None,
        data=body,
        response_code=status.HTTP_200_OK,
        success=True,
    )
