from collections.abc import Sequence

from app.db.models.language import Language
from app.repositories.language_repository import LanguageRepository
from app.schemas.language import (
    LanguageCreate,
    LanguageUpdate,
)


class LanguageService:

    def __init__(
            self,
            repository: LanguageRepository,
    ):
        self.repository = repository

    def get(
            self,
            lang_id: int,
    ) -> Language | None:
        """
        Get a language by ID.
        """
        return self.repository.get(lang_id)

    def get_by_code(
            self,
            lang_code: str,
    ) -> Language | None:
        """
        Get a language by code.
        """
        return self.repository.get_by_code(lang_code)

    def get_all(
            self,
    ) -> Sequence[Language]:
        """
        Get all languages.
        """
        return self.repository.get_all()

    def create(
            self,
            create_data: LanguageCreate,
    ) -> Language:
        """
        Create a new language.
        """
        return self.repository.create(create_data)

    def update(
            self,
            db_obj: Language,
            update_data: LanguageUpdate,
    ) -> Language:
        """
        Update a language.
        """
        return self.repository.update(
            db_obj,
            update_data,
        )

    def delete(
            self,
            db_obj: Language,
    ) -> None:
        """
        Delete a language.
        """
        self.repository.delete(db_obj)
