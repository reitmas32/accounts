from uuid import UUID

from shared.app.entities.base_entity import EntityBase
from shared.app.enums.platform_login import PlatformsLogin


class PlatformEntity(EntityBase):
    user_id: UUID
    external_id: str
    active: bool = False
    type: PlatformsLogin

