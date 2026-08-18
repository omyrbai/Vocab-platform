from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.auth_provider import AuthProvider


class UserIdentityCreate(BaseModel):
    user_id: int
    provider: AuthProvider

    provider_user_id: str = Field(
        min_length=1,
        max_length=255,
    )
    email: str | None = Field(
        default=None,
        max_length=255,
    )
    password_hash: str | None = Field(
        default=None,
        max_length=255,
    )


class UserIdentityRead(BaseModel):
    identity_id: int
    user_id: int
    provider: str
    provider_user_id: str
    email: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )