from pydantic import BaseModel

from shared.app.enums.platform_login import PlatformsLogin


class SignupPlatformDto(BaseModel):
    platform: PlatformsLogin
    external_id: str
    token: str
    user_name: str | None = None
    metadata: dict | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "platform": "google",
                    "external_id": "123456789",
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                }
            ]
        }
    }
