from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, SmallInteger, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.term import Term
    from app.db.models.user import User

class Language(Base):
    __tablename__ = "languages"

    lang_id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        autoincrement=True,
    )

    lang_code: Mapped[str] = mapped_column(
        String(2),
        unique=True,
        nullable=False,
    )

    language_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    native_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # Relationship

    source_terms: Mapped[list["Term"]] = relationship(
        foreign_keys="Term.src_lang_id",
        back_populates="source_language",
    )

    target_terms: Mapped[list["Term"]] = relationship(
        foreign_keys="Term.trg_lang_id",
        back_populates="target_language",
    )

    source_users: Mapped[list["User"]] = relationship(
        foreign_keys="User.src_lang_id",
        back_populates="source_language",
    )

    target_users: Mapped[list["User"]] = relationship(
        foreign_keys="User.trg_lang_id",
        back_populates="target_language",
    )


    def __repr__(self) -> str:
        return (
            f"Language("
            f"lang_id={self.lang_id}, "
            f"lang_code='{self.lang_code}', "
            f"language_name='{self.language_name}')"
        )