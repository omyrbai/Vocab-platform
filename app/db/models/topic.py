from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    UniqueConstraint,
    ForeignKey,
    String,
    Text,
    TIMESTAMP,
    text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    topic_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    parent_topic_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "topics.topic_id",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    name:  Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description:  Mapped[str | None] = mapped_column(
        Text,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationships

    parent: Mapped["Topic | None"] = relationship(
        remote_side=[topic_id],
        back_populates="children",
    )

    children: Mapped[list["Topic"]] = relationship(
        back_populates="parent",
    )

    terms: Mapped[list["Term"]] = relationship(
        back_populates="topic",
    )

    __table_args__ = (
        UniqueConstraint(
            "parent_topic_id",
            "name",
            name="uq_topic_parent_name",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"Topic("
            f"topic_id={self.topic_id}, "
            f"name='{self.name}')"
        )