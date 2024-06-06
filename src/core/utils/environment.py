from enum import Enum


class EnvironmentsTypes(Enum):
    LOCAL = "local", "local"
    DEVELOPMENT = "development", "dev"
    STAGING = "staging", "stg"
    PRODUCTION = "production", "prd"
    TESTING = "testing", "test"
    DOCKER = "docker", "docker"

    @classmethod
    def _is_valid_env(cls, value: str) -> bool:
        list_envs = cls._get_valid_envs()
        return value in list_envs

    @classmethod
    def _get_valid_envs(cls):
        return [member.value[0] for member in cls]

    @classmethod
    def check_env_value(cls, value: str):
        if not cls._is_valid_env(value):
            raise ValueError(
                f"{value} is not a valid Environment value. Valid values are: {', '.join(cls._get_valid_envs())}"
            )

    @classmethod
    def get_env_file_name(cls, env_name):
        prefix_files = ".env"
        for member in cls:
            if member.value[0] == env_name:
                return f"{prefix_files}.{member.value[1]}"
        raise ValueError(f"{env_name} don't have any env file associative")
