from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    telegram_id: int | None = None

    username: str | None = Field(
        default=None,
        max_length=255,
    )

    first_name: str = Field(
        min_length=1,
        max_length=255,
    )

    src_lang_id: int | None = None

    trg_lang_id: int | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    telegram_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    src_lang_id: int | None = None
    trg_lang_id: int | None = None


class UserRead(UserBase):
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )