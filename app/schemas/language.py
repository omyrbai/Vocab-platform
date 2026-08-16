from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LanguageBase(BaseModel):
    lang_code: str = Field(
        min_length=2,
        max_length=2,
    )
    language_name: str = Field(
        min_length=1,
        max_length=100,
    )
    native_name: str = Field(
        min_length=1,
        max_length=100,
    )


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(BaseModel):
    lang_code: str | None = Field(
        default=None,
        min_length=2,
        max_length=2,
    )
    language_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    native_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )


class LanguageRead(LanguageBase):
    lang_id: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )