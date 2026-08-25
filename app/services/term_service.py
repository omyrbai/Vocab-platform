from collections.abc import Sequence

from app.enums.import_action import ImportAction
from app.exceptions import ConflictError, NotFoundError

from app.repositories.language_repository import LanguageRepository
from app.repositories.term_repository import TermRepository
from app.repositories.topic_repository import TopicRepository
from app.schemas.term import (
    TermCreate,
    TermUpdate,
)

from app.db.models.term import Term

class TermService:

    def __init__(
            self,
            term_repository: TermRepository,
            language_repository: LanguageRepository,
            topic_repository: TopicRepository,
    ):
        self.term_repository = term_repository
        self.language_repository = language_repository
        self.topic_repository = topic_repository

    def create(
        self,
        user_id: int | None,
        create_data: TermCreate,
        *,
        commit: bool = True,
    ) -> Term:
        """
        Create a new term.
        """

        src_language = self.language_repository.get(
            create_data.src_lang_id
        )

        if src_language is None:
            raise NotFoundError(
                "Source language not found."
            )

        trg_language = self.language_repository.get(
            create_data.trg_lang_id
        )

        if trg_language is None:
            raise NotFoundError(
                "Target language not found."
            )

        topic = self.topic_repository.get(
            create_data.topic_id
        )

        if topic is None:
            raise NotFoundError(
                "Topic not found."
            )

        if (
            user_id is not None
            and topic.user_id != user_id
        ):
            raise NotFoundError(
                "Topic not found."
            )

        existing_term = self.term_repository.find_duplicate(
            topic_id=create_data.topic_id,
            src_lang_id=create_data.src_lang_id,
            trg_lang_id=create_data.trg_lang_id,
            term=create_data.term,
        )

        if existing_term is not None:
            raise ConflictError(
                "Term already exists in the selected context."
            )

        return self.term_repository.create(
            create_data,
            commit=commit,
        )

    def update(
        self,
        user_id: int | None,
        term_id: int,
        update_data: TermUpdate,
        *,
        commit: bool = True,
    ) -> Term:
        db_obj = self.get(
            user_id=user_id,
            term_id=term_id,
        )

        if db_obj is None:
            raise NotFoundError(
                "Term not found."
            )

        src_lang_id = (
            update_data.src_lang_id
            if update_data.src_lang_id is not None
            else db_obj.src_lang_id
        )

        trg_lang_id = (
            update_data.trg_lang_id
            if update_data.trg_lang_id is not None
            else db_obj.trg_lang_id
        )

        topic_id = (
            update_data.topic_id
            if update_data.topic_id is not None
            else db_obj.topic_id
        )

        if topic_id is not None:
            topic = self.topic_repository.get(topic_id)

            if topic is None:
                raise NotFoundError(
                    "Topic not found."
                )

            if (
                user_id is not None
                and topic.user_id != user_id
            ):
                raise NotFoundError(
                    "Topic not found."
                )

        term = (
            update_data.term
            if update_data.term is not None
            else db_obj.term
        )

        src_language = self.language_repository.get(src_lang_id)

        if src_language is None:
            raise NotFoundError(
                "Source language not found."
            )

        trg_language = self.language_repository.get(trg_lang_id)

        if trg_language is None:
            raise NotFoundError(
                "Target language not found."
            )

        existing_term = self.term_repository.find_duplicate(
            topic_id=topic_id,
            src_lang_id=src_lang_id,
            trg_lang_id=trg_lang_id,
            term=term,
            exclude_term_id=db_obj.term_id
        )

        if existing_term is not None:
            raise ConflictError(
                "Term already exists in the selected context."
            )

        return self.term_repository.update(
            db_obj,
            update_data,
            commit=commit,
        )

    def delete(
        self,
        user_id: int | None,
        term_id: int,
        *,
        commit: bool = True,
    ) -> None:
        db_obj = self.get(
            user_id=user_id,
            term_id=term_id,
        )

        if db_obj is None:
            raise NotFoundError(
                "Term not found."
            )

        self.term_repository.delete(
            db_obj,
            commit=commit,
        )

    def get(
        self,
        user_id: int | None,
        term_id: int,
    ) -> Term | None:
        """
        Get a term.

        If user_id is provided, the term must belong
        to a topic owned by that user.

        If user_id is None, return the term regardless
        of its topic owner.
        """
        if user_id is None:
            return self.term_repository.get(term_id)

        return self.term_repository.get_by_id_for_user(
            term_id=term_id,
            user_id=user_id,
        )

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

        return self.term_repository.get_by_term(
            term=term,
            user_id=user_id,
        )

    def get_by_topic_ids(
        self,
        topic_ids: Sequence[int],
        user_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms belonging to the specified topics.

        If user_id is provided, only topics owned by that user
        are included.
        """

        return self.term_repository.get_by_topic_ids(
            topic_ids=topic_ids,
            user_id=user_id,
        )

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


        return self.term_repository.get_all(
            user_id=user_id,
        )


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

        return self.term_repository.get_by_topic(
            topic_id=topic_id,
            user_id=user_id,
        )

    def get_by_languages(
            self,
            *,
            user_id: int | None = None,
            src_lang_id: int | None = None,
            trg_lang_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms filtered by source and target language.
        """
        return self.term_repository.get_by_languages(
            user_id=user_id,
            src_lang_id=src_lang_id,
            trg_lang_id=trg_lang_id,
        )

    def get_filtered(
        self,
        *,
        user_id: int | None = None,
        topic_id: int | None = None,
        src_lang_id: int | None = None,
        trg_lang_id: int | None = None,
    ) -> Sequence[Term]:
        """
        Get terms filtered by topic and/or language pair.
        """
        return self.term_repository.get_filtered(
            user_id=user_id,
            topic_id=topic_id,
            src_lang_id=src_lang_id,
            trg_lang_id=trg_lang_id,
        )

    def term_count_by_user(
        self,
        user_id: int,
    ) -> int:
        """
        Count all terms belonging to topics owned by the user.
        """
        return self.term_repository.term_count_by_user(
            user_id=user_id,
        )

    def find_duplicate(
        self,
        topic_id: int,
        src_lang_id: int,
        trg_lang_id: int,
        term: str,
    ) -> Term | None:
        """
        Find an existing term with the same unique key.
        """

        return self.term_repository.find_duplicate(
            topic_id=topic_id,
            src_lang_id=src_lang_id,
            trg_lang_id=trg_lang_id,
            term=term,
        )

    def _has_changes(
        self,
        db_obj: Term,
        create_data: TermCreate,
    ) -> bool:
        """
        Check whether the imported data differs from
        the existing database record.
        """

        return any([
            db_obj.gender != create_data.gender,
            db_obj.definition != create_data.definition,
            db_obj.example != create_data.example,
            db_obj.translation != create_data.translation,
            db_obj.pronunciation != create_data.pronunciation,
        ])

    def upsert(
        self,
        user_id: int,
        create_data: TermCreate,
        *,
        commit: bool = True,
    ) -> tuple[
        Term,
        ImportAction,
    ]:
        """
        Create a new term or update an existing one.
        """

        db_obj = self.find_duplicate(
            topic_id=create_data.topic_id,
            src_lang_id=create_data.src_lang_id,
            trg_lang_id=create_data.trg_lang_id,
            term=create_data.term,
        )

        if db_obj is None:
            return (
                self.create(
                    user_id=user_id,
                    create_data=create_data,
                    commit=commit,
                ),
                ImportAction.CREATED,
            )

        if not self._has_changes(
                db_obj,
                create_data,
        ):
            return (
                db_obj,
                ImportAction.SKIPPED,
            )

        update_data = TermUpdate(
            **create_data.model_dump(
                exclude={
                    "topic_id",
                    "src_lang_id",
                    "trg_lang_id",
                    "term",
                }
            )
        )

        return (
            self.update(
                user_id=user_id,
                term_id=db_obj.term_id,
                update_data=update_data,
                commit=commit,
            ),
            ImportAction.UPDATED,
        )