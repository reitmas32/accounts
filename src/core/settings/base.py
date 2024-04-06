# Standard Library
import os
import sys
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
    POSTGRESQL_URL: PostgresDsn

    # Sentry settings
    # ----------------------------------------------------------------
    SENTRY_DSN: str

    # Manager email
    # ----------------------------------------------------------------
    EMAIL_SENDER: str
    EMAIL_SENDER_PASSWORD: str

    # Project Constants
    # ----------------------------------------------------------------
    PROJECT_NAME: str = "Accounts"
    TEAM_NAME: str = "R2"
    TIME_ZONE: str = "utc"
    TIME_ZONE_UTC: str = "utc"
    DATE_FORMAT: str = "%Y-%m-%d"
    API_V1: str = "v1"

    # Password settings
    # ----------------------------------------------------------------
    HASHING_ALGORITHM : HashingAlgorithmsEnum = HashingAlgorithmsEnum.BCRYPT

    # Token JWT settings
    # ----------------------------------------------------------------
    TIME_SECONDS_EXPIRE_TOKEN_JWT: int = 60 * 60 * 24
    ALGORITHM_JWT: JWTAlgorithmsEnum = JWTAlgorithmsEnum.RS256


    # Authenticate settings
    # ----------------------------------------------------------------
    TIME_SECONDS_EXPIRE_CODE_VALIDATE_EMAIL:int = 60 * 60 * 24 * 30
    TIME_SECONDS_EXPIRE_CODE_2FA:int = 60 * 1
    LENGHT_CODE_VALIDATE_EMAIL : int = 4
    LENGHT_CODE_2FA: int = 4
