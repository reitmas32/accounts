from core.settings import settings
from shared.databases.enums import DataBasesEnum

if settings.ENGINE_DB == DataBasesEnum.MYSQL:
    from shared.databases.mysql.models.base_model import Base, BaseModelClass
else:
    from shared.databases.postgres.models.base_model import (  # noqa: F401
        Base,
        BaseModelClass,
    )
