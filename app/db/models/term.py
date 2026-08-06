from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    TIMESTAMP,
    UniqueConstraint,
    text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Term(Base):
    __tablename__ = "terms"

    term_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    topic_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "topics.topic_id",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    src_lang_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "languages.lang_id",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    trg_lang_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            "languages.lang_id",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    term: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    pronunciation: Mapped[str | None] = mapped_column(
        String(255),
    )

    definition: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    example: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    translation: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    #relationship
    source_language: Mapped["Language"] = relationship(
        foreign_keys=[src_lang_id],
        back_populates="source_terms",
    )

    target_language: Mapped["Language"] = relationship(
        foreign_keys=[trg_lang_id],
        back_populates="target_terms",
    )

    topic: Mapped["Topic | None"] = relationship(
        back_populates="terms"
    )

    __table_args__ = (
        UniqueConstraint(
            "topic_id",
            "src_lang_id",
            "trg_lang_id",
            "term",
            name="uq_term",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"Term(term_id={self.term_id}, "
            f"term='{self.term}')"
        )