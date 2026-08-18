from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenCreate(BaseModel):
    user_id: int
    token_hash: str = Field(
        min_length=1,
        max_length=255,
    )
    expires_at: datetime


class RefreshTokenRead(BaseModel):
    refresh_token_id: int
    user_id: int
    expires_at: datetime
    created_at: datetime
    revoked_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )