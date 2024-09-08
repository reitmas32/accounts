# Standard Library
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv

# Third Party Stuff
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pydantic_settings import SettingsConfigDict

from core.settings.enum import HashingAlgorithmsEnum, JWTAlgorithmsEnum
from core.utils.environment import EnvironmentsTypes

LIST_PATH_TO_ADD = []
if LIST_PATH_TO_ADD:
    sys.path.extend(LIST_PATH_TO_ADD)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENVS_DIR = BASE_DIR.parent / ".envs"
ENV_BASE_FILE_PATH = ENVS_DIR / ".env.base"
load_dotenv(ENV_BASE_FILE_PATH)
ENVIRONMENT = os.environ.get("ENVIRONMENT")
EnvironmentsTypes.check_env_value(ENVIRONMENT)
ENV_FILE_PATH = ENVS_DIR / EnvironmentsTypes.get_env_file_name(ENVIRONMENT)


class Settings(PydanticBaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore", case_sensitive=True)
    ENVIRONMENT: str = ENVIRONMENT
    CORS_ORIGINS: ClassVar[list[str]] = ["*"]
    # Database settings
    # ----------------------------------------------------------------
    POSTGRES_DSN: PostgresDsn

    # Sentry settings
    # ----------------------------------------------------------------
    SENTRY_DSN: str

    # Manager email
    # ----------------------------------------------------------------
    EMAIL_SENDER: str
    EMAIL_SENDER_PASSWORD: str
    EMAIL_CLIENT: str

    # Auth-Manager
    # ----------------------------------------------------------------
    AUTH_SERVICE_API_HOST: str
    AUTHTENTICATION_ACTIVE: bool = False
    PUBLIC_ENDPOINTS: list[str] = [
        "/accounts/health",
        "/accounts/docs",
        "/accounts/favicon.ico",
        "/accounts/openapi.json",
        "/accounts",
        "/health",
        "/docs",
        "/favicon.ico",
        "/openapi.json",
        "",
    ]
    AUTH_SERVICE_API_VERSION: str = "v1"
    AUTH_SERVICE_API_PREFIX: str = "services"
    # Project Constants
    # ----------------------------------------------------------------
    PROJECT_NAME: str = "Accounts"
    PROJECT_ID: str = "API0002"
    TEAM_NAME: str = "R2"
    TIME_ZONE: str = "utc"
    TIME_ZONE_UTC: str = "utc"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    API_V1: str = "v1"

    # Password settings
    # ----------------------------------------------------------------
    HASHING_ALGORITHM: HashingAlgorithmsEnum = HashingAlgorithmsEnum.BCRYPT

    # Token JWT settings
    # ----------------------------------------------------------------
    TIME_SECONDS_EXPIRE_TOKEN_JWT: int = 60 * 60 * 24
    ALGORITHM_JWT: JWTAlgorithmsEnum = JWTAlgorithmsEnum.RS256

    # JWT
    PRIVATE_KEY_JWT: str
    PUBLIC_KEY_JWT: str

    # Authenticate settings
    # ----------------------------------------------------------------
    TIME_SECONDS_EXPIRE_CODE_VALIDATE_EMAIL: int = 60 * 60 * 24 * 30
    TIME_SECONDS_EXPIRE_CODE_2FA: int = 60 * 1
    TIME_SECONDS_EXPIRE_VERIFICATION_CODE: int = 20 * 60
    LENGHT_CODE_VALIDATE_EMAIL: int = 4
    LENGHT_CODE_2FA: int = 4

    # Pagination settings
    # ----------------------------------------------------------------
    DEFAULT_PAGE_SIZE: int = 30
    DEFAULT_ORDER_FIELD: str = "created"
    TIMESTAP: datetime = datetime.now().astimezone().strftime(format=DATE_TIME_FORMAT)
