
from fastapi.security import OAuth2PasswordBearer
from core.utils.jwt import JWTHandler,TokenDataSchema
from fastapi import (
    Depends
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_data_token(token: str = Depends(oauth2_scheme)):
    payload: TokenDataSchema = JWTHandler.validate_token(token=token)
    return payload