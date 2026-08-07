from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.term import Term
from app.repositories.base_repository import BaseRepository
from app.schemas.term import (
    TermCreate,
    TermUpdate,
)


class TermRepository(
    BaseRepository[
        Term,
        TermCreate,
        TermUpdate,
    ]
):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session=session,
            model=Term,
            pk_field="term_id",
        )

    def get_by_term(
        self,
        term: str,
    ) -> Sequence[Term]:
        """
        Get a term by term.
        """

        stmt = (
            select(self.model)
            .where(self.model.term == term)
        )

        return self.session.scalars(stmt).all()

    def get_all(
        self,
    ) -> Sequence[Term]:
        """
        Get all terms.
        """

        stmt = (
            select(self.model)
            .order_by(self.model.term)
        )

        return self.session.scalars(stmt).all()

    def get_by_topic(
        self,
        topic_id: int
    ) -> Sequence[Term]:
        """
        Get all terms which contains the topic.
        """

        stmt = (
            select(self.model)
            .where(self.model.topic_id == topic_id)
            .order_by(self.model.term)
        )

        return self.session.scalars(stmt).all()

    def get_by_topic_ids(
        self,
        topic_ids: Sequence[int],
    ) -> Sequence[Term]:

        stmt = (
            select(self.model)
            .where(
                self.model.topic_id.in_(topic_ids)
            )
            .order_by(self.model.term)
        )

        return self.session.scalars(stmt).all()

    def get_by_languages(
        self,
        *,
        src_lang_id: int | None = None,
        trg_lang_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms filtered by source and/or target language.
        """

        if src_lang_id is None and trg_lang_id is None:
            raise ValueError(
                "Either src_lang_id or trg_lang_id must be provided."
            )

        stmt = select(self.model)

        if src_lang_id is not None:
            stmt = stmt.where(
                self.model.src_lang_id == src_lang_id
            )

        if trg_lang_id is not None:
            stmt = stmt.where(
                self.model.trg_lang_id == trg_lang_id
            )

        stmt = stmt.order_by(self.model.term)

        return self.session.scalars(stmt).all()

    def find_duplicate(
        self,
        *,
        topic_id: int | None,
        src_lang_id: int,
        trg_lang_id: int,
        term: str,
        exclude_term_id: int | None = None,
    ) -> Term | None:
        """
        Find a term with the same context.

        Returns the existing term if a duplicate exists,
        otherwise returns None.
        """

        stmt = select(self.model)

        stmt = stmt.where(
            self.model.src_lang_id == src_lang_id,
            self.model.trg_lang_id == trg_lang_id,
            self.model.term == term,
        )

        if topic_id is not None:
            stmt = stmt.where(
                self.model.topic_id == topic_id
            )
        else:
            stmt = stmt.where(
                self.model.topic_id.is_(None)
            )

        if exclude_term_id is not None:
            stmt = stmt.where(
                self.model.term_id != exclude_term_id
            )

        return self.session.scalar(stmt)
