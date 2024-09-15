from enum import Enum

from pydantic import BaseModel


class EnvironmentModel(BaseModel):
    env_name: str
    suffix: str


class EnvironmentsTypes(Enum):
    LOCAL = EnvironmentModel(env_name="local", suffix="local")
    DEVELOPMENT = EnvironmentModel(env_name="development", suffix="dev")
    STAGING = EnvironmentModel(env_name="staging", suffix="stg")
    PRODUCTION = EnvironmentModel(env_name="production", suffix="prd")
    TESTING = EnvironmentModel(env_name="testing", suffix="test")
    DOCKER = EnvironmentModel(env_name="docker", suffix="docker")

    @classmethod
    def _is_valid_env(cls, value: str) -> bool:
        list_envs = cls._get_valid_envs()
        return value in list_envs

    @classmethod
    def _get_valid_envs(cls):
        return [member.value.env_name for member in cls]

    @classmethod
    def validate(cls, value: str):
        if not cls._is_valid_env(value):
            raise ValueError(
                f"{value} is not a valid Environment value. Valid values are: {', '.join(cls._get_valid_envs())}"
            )

    @classmethod
    def get_env_file_name(cls, env_name):
        prefix_files = ".env"
        for member in cls:
            if member.value.env_name == env_name:
                return f"{prefix_files}.{member.value.suffix}"
        raise ValueError(f"{env_name} don't have any env file associative")
