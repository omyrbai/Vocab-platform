from collections.abc import Sequence

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
            create_data: TermCreate
    ) -> Term:
        """
        Create a new term.
        """
        src_language = self.language_repository.get(
            create_data.src_lang_id
        )

        if src_language is None:
            raise ValueError(
                "Source language not found."
            )

        trg_language = self.language_repository.get(
            create_data.trg_lang_id
        )

        if trg_language is None:
            raise ValueError(
                "Target language not found."
            )

        if create_data.topic_id is not None:
            topic = self.topic_repository.get(
                create_data.topic_id
            )

            if topic is None:
                raise ValueError(
                    "Topic not found."
                )

        existing_term = self.term_repository.find_duplicate(
            topic_id=create_data.topic_id,
            src_lang_id=create_data.src_lang_id,
            trg_lang_id=create_data.trg_lang_id,
            term=create_data.term,
        )

        if existing_term is not None:
            raise ValueError(
                "Term already exists in the selected context."
            )

        return self.term_repository.create(
            create_data
        )

    def update(
            self,
            term_id: int,
            update_data: TermUpdate,
    ) -> Term:
        db_obj = self.term_repository.get(term_id)

        if db_obj is None:
            raise ValueError(
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
                raise ValueError(
                    "Topic not found."
                )

        term = (
            update_data.term
            if update_data.term is not None
            else db_obj.term
        )

        src_language = self.language_repository.get(src_lang_id)

        if src_language is None:
            raise ValueError(
                "Source language not found."
            )

        trg_language = self.language_repository.get(trg_lang_id)

        if trg_language is None:
            raise ValueError(
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
            raise ValueError(
                "Term already exists in the selected context."
            )

        return self.term_repository.update(
            db_obj,
            update_data,
        )

    def delete(
            self,
            term_id: int,
    ) -> None:
        db_obj = self.term_repository.get(term_id)

        if db_obj is None:
            raise ValueError(
                "Term not found."
            )

        self.term_repository.delete(db_obj)

    def get(
            self,
            term_id: int,
    ) -> Term | None:
        """
        Get a term.
        """
        return self.term_repository.get(term_id)

    def get_by_term(
        self,
        term: str
    ) -> Sequence[Term]:
        """
        Get terms by term.
        """

        return self.term_repository.get_by_term(term)

    def get_all(
            self,
    ) -> Sequence[Term]:
        """
        Get all terms.
        """
        return self.term_repository.get_all()


    def get_by_topic(
            self,
            topic_id: int
    ) -> Sequence[Term]:
        """
        Get all terms by a specific topic.
        """
        return self.term_repository.get_by_topic(topic_id)

    def get_by_languages(
            self,
            src_lang_id: int,
            trg_lang_id: int,
    ) -> Sequence[Term]:
        """
        Get terms filtered by source and target language.
        """
        return self.term_repository.get_by_languages(
            src_lang_id=src_lang_id,
            trg_lang_id=trg_lang_id,
        )
