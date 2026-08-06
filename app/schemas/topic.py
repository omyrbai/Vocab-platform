from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TopicBase(BaseModel):
    parent_topic_id: int | None = None

    name: str = Field(
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
    )


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    parent_topic_id: int | None = None
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        min_length=1,
    )


class TopicRead(TopicBase):
    topic_id: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )