from datetime import timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError, decode
from pydantic import BaseModel, ValidationError

from core.settings import settings
from core.utils.responses import get_current_date_time_to_app_standard


class TokenDataSchema(BaseModel):
    user_id: str


class JWTHandler:
    @staticmethod
    def create_token(data: TokenDataSchema) -> str:
        to_encode = data.model_dump()
        expire = get_current_date_time_to_app_standard() + timedelta(seconds=settings.TIME_SECONDS_EXPIRE_TOKEN_JWT)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.PRIVATE_KEY_JWT, algorithm=settings.ALGORITHM_JWT.value)

    @staticmethod
    def validate_token(token: str) -> TokenDataSchema:
        try:
            payload = decode(token, settings.PUBLIC_KEY_JWT, algorithms=[settings.ALGORITHM_JWT.value])
            return TokenDataSchema(**payload)
        except ExpiredSignatureError:
            raise ValueError("Token has expired")
        except InvalidTokenError:
            raise ValueError("Invalid token")
        except ValidationError as e:
            raise ValueError(f"Invalid token data: {e}")
