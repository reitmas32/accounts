from uuid import UUID

from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from core.settings import log
from core.settings.database import get_session
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.get(
    "/{user_id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_one(
    request: Request,
    user_id: UUID,
    session: Session = Depends(get_session),
):
    log.info("Get User")
    return EnvelopeResponse(
        data={"user_id": user_id},
        response_code=status.HTTP_200_OK,
        success=True,
    )
