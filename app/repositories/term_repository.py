from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.term import Term
from app.db.models.topic import Topic
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

    def get_by_id_for_user(
            self,
            term_id: int,
            user_id: int,
    ) -> Term | None:
        """
        Get a term belonging to a topic owned by the specified user.
        """

        stmt = (
            select(self.model)
            .join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            )
            .where(
                self.model.term_id == term_id,
                Topic.user_id == user_id,
            )
        )

        return self.session.scalar(stmt)

    def get_by_term(
        self,
        term: str,
        user_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms by term.

        If user_id is provided, only terms whose topics
        belong to that user are returned.
        """

        stmt = select(self.model)

        if user_id is not None:
            stmt = stmt.join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id
            )

        stmt = stmt.where(
            self.model.term == term,
        ).order_by(
            self.model.term,
        )

        return self.session.scalars(stmt).all()

    def get_all(
        self,
        user_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get all terms.

        If user_id is provided, return only terms whose
        topics belong to that user.

        If user_id is None, return all terms.
        """

        stmt = select(self.model)

        if user_id is not None:
            stmt = stmt.join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id,
            )

        stmt = stmt.order_by(
            self.model.term,
        )

        return self.session.scalars(stmt).all()

    def get_by_topic(
        self,
        topic_id: int,
        user_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms belonging to a topic.

        If user_id is provided, the topic must belong
        to that user.

        If user_id is None, return terms regardless
        of topic owner.
        """

        stmt = select(self.model)

        if user_id is not None:
            stmt = stmt.join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id,
            )

        stmt = stmt.where(
            self.model.topic_id == topic_id
        ).order_by(
            self.model.term
        )

        return self.session.scalars(stmt).all()

    def get_by_topic_ids(
        self,
        topic_ids: Sequence[int],
        user_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms belonging to the specified topics.

        If user_id is provided, only topics owned by that
        user are included.

        If user_id is None, topics from any user are included.
        """

        stmt = select(self.model)

        if user_id is not None:
            stmt = stmt.join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id,
            )

        stmt = stmt.where(
            self.model.topic_id.in_(topic_ids)
        ).order_by(
            self.model.term
        )

        return self.session.scalars(stmt).all()

    def term_count_by_user(
        self,
        user_id: int,
    ) -> int:
        """
        Count all terms belonging to topics owned by the user.
        """
        stmt = (
            select(func.count(self.model.term_id))
            .join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id,
            )
        )

        return self.session.scalar(stmt) or 0


    def get_by_languages(
        self,
        *,
        user_id: int | None = None,
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

        if user_id is not None:
            stmt = stmt.join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id,
            )


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

    def get_filtered(
            self,
            *,
            user_id: int | None = None,
            topic_id: int | None = None,
            src_lang_id: int | None = None,
            trg_lang_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms filtered by user, topic, and/or language pair.

        If user_id is provided, return only terms whose
        topic belongs to that user.

        If user_id is None, return terms regardless of owner.
        """
        stmt = select(self.model)

        if user_id is not None:
            stmt = stmt.join(
                Topic,
                self.model.topic_id == Topic.topic_id,
            ).where(
                Topic.user_id == user_id,
            )

        if topic_id is not None:
            stmt = stmt.where(
                self.model.topic_id == topic_id
            )

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
        topic_id: int,
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
            self.model.topic_id == topic_id,
            self.model.src_lang_id == src_lang_id,
            self.model.trg_lang_id == trg_lang_id,
            self.model.term == term,
        )

        if exclude_term_id is not None:
            stmt = stmt.where(
                self.model.term_id != exclude_term_id
            )

        return self.session.scalar(stmt)
