from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TermBase(BaseModel):
    topic_id: int | None = None
    src_lang_id: int
    trg_lang_id: int
    term: str = Field(
        min_length=1,
        max_length=255,
    )
    pronunciation: str | None = Field(
        default=None,
        max_length=255,
    )
    definition: str = Field(
        min_length=1,
    )
    example: str = Field(
        min_length=1,
    )
    translation: str = Field(
        min_length=1,
        max_length=255,
    )


class TermCreate(TermBase):
    pass


class TermUpdate(BaseModel):
    topic_id: int | None = None
    src_lang_id: int | None = None
    trg_lang_id: int | None = None
    term: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    pronunciation: str | None = Field(
        default=None,
        max_length=255,
    )
    definition: str | None = Field(
        default=None,
        min_length=1,
    )
    example: str | None = Field(
        default=None,
        min_length=1,
    )
    translation: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class TermRead(TermBase):
    term_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )