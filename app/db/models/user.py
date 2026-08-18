from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    SmallInteger,
    ForeignKey,
    String,
    func,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base
from app.db.models.language import Language

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user_identity import UserIdentity
    from app.db.models.refresh_token import RefreshToken
    from app.db.models.topic import Topic

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger,
        unique=True,
        nullable=True,
    )

    username:  Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    first_name:  Mapped[str] = mapped_column(
        String(255),
    )

    src_lang_id: Mapped[int | None] = mapped_column(
        SmallInteger,
        ForeignKey("languages.lang_id", ondelete="SET NULL"),
        nullable=True,
    )

    trg_lang_id: Mapped[int | None] = mapped_column(
        SmallInteger,
        ForeignKey("languages.lang_id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    # Relationships

    source_language: Mapped[Language | None] = relationship(
        foreign_keys=[src_lang_id],
        back_populates="source_users",
    )

    target_language: Mapped[Language | None] = relationship(
        foreign_keys=[trg_lang_id],
        back_populates="target_users",
    )

    topics: Mapped[list["Topic"]] = relationship(
        back_populates="owner",
    )

    identities: Mapped[list["UserIdentity"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"User("
            f"user_id={self.user_id}, "
            f"telegram_id={self.telegram_id}, "
            f"username='{self.username}', "
            f"first_name='{self.first_name}')"
        )