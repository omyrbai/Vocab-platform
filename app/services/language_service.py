from collections.abc import Sequence

from app.db.models.language import Language
from app.exceptions import ConflictError, NotFoundError
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

        existing_language = self.find_duplicate(
            lang_code=create_data.lang_code,
            language_name=create_data.language_name,
        )

        if existing_language is not None:
            raise ConflictError(
                "Language with this code already exists."
            )

        return self.repository.create(create_data)

    def update(
            self,
            db_obj: Language,
            update_data: LanguageUpdate,
    ) -> Language:
        """
        Update a language.
        """

        lang_code = (
            update_data.lang_code
            if update_data.lang_code is not None
            else db_obj.lang_code
        )
        language_name = (
            update_data.language_name
            if update_data.language_name is not None
            else db_obj.language_name
        )
        existing_language = self.find_duplicate(
            lang_code=lang_code,
            language_name=language_name,
            exclude_lang_id=db_obj.lang_id,
        )

        if existing_language is not None:
            raise ConflictError(
                "Language with the same code or name already exists."
            )

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

    def find_duplicate(
        self,
        lang_code: str,
        language_name: str,
        exclude_lang_id: int | None = None,
    ) -> Language | None:
        """
        Find a language with the same code.
        """

        return self.repository.find_duplicate(
            lang_code=lang_code,
            language_name=language_name,
            exclude_lang_id=exclude_lang_id,
        )