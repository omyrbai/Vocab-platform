from collections.abc import Sequence

from app.db.models.user import User
from app.exceptions import ConflictError, NotFoundError
from app.repositories.language_repository import LanguageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserService:

    def __init__(
        self,
        repository: UserRepository,
        language_repository: LanguageRepository,
    ):
        self.repository = repository
        self.language_repository = language_repository

    def get(
            self,
            user_id: int,
    ) -> User | None:
        """
        Get a user by ID.
        """

        return self.repository.get(user_id)

    def get_by_telegram_id(
            self,
            telegram_id: int,
    ) -> User | None:
        """
        Get a user by telegram ID.
        """
        return self.repository.get_by_telegram_id(telegram_id)

    def get_all(
            self,
    ) -> Sequence[User]:
        """
        Get all users.
        """
        return self.repository.get_all()

    def get_by_username(
            self,
            username: str,
    ) -> User | None:
        """
        Get a user by username.
        """

        return self.repository.get_by_username(username)

    def create(
            self,
            create_data: UserCreate,
    ) -> User:
        """
        Create a new user.
        """

        if create_data.telegram_id is not None:
            existing_user = self.repository.get_by_telegram_id(
                create_data.telegram_id
            )

            if existing_user is not None:
                raise ConflictError(
                    "Telegram user already exists."
                )
        if create_data.username is not None:
            existing_user = self.repository.get_by_username(
                create_data.username
            )

            if existing_user is not None:
                raise ConflictError(
                    "Username already exists."
                )

        if create_data.src_lang_id is not None:
            language = self.language_repository.get(
                create_data.src_lang_id
            )

            if language is None:
                raise NotFoundError(
                    "Source language not found."
                )

        if create_data.trg_lang_id is not None:
            language = self.language_repository.get(
                create_data.trg_lang_id
            )

            if language is None:
                raise NotFoundError(
                    "Target language not found."
                )

        return self.repository.create(create_data)

    def update(
            self,
            user_id: int,
            update_data: UserUpdate,
    ) -> User:
        """
        Update a user.
        """

        db_obj = self.repository.get(user_id)

        if db_obj is None:
            raise NotFoundError(
                "User not found."
            )
        telegram_id = (
            update_data.telegram_id
            if update_data.telegram_id is not None
            else db_obj.telegram_id
        )

        username = (
            update_data.username
            if update_data.username is not None
            else db_obj.username
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

        if telegram_id is not None:
            existing_user = self.repository.get_by_telegram_id(
                telegram_id
            )

            if (
                existing_user is not None
                and existing_user.user_id != db_obj.user_id
            ):
                raise ConflictError(
                    "Telegram user already exists."
                )

        if username is not None:
            existing_user = self.repository.get_by_username(
                username
            )

            if (
                existing_user is not None
                and existing_user.user_id != db_obj.user_id
            ):
                raise ConflictError(
                    "Username already exists."
                )

        if src_lang_id is not None:
            language = self.language_repository.get(
                src_lang_id
            )

            if language is None:
                raise NotFoundError(
                    "Source language not found."
                )

        if trg_lang_id is not None:
            language = self.language_repository.get(
                trg_lang_id
            )

            if language is None:
                raise NotFoundError(
                    "Target language not found."
                )

        return self.repository.update(
            db_obj,
            update_data,
        )

    def delete(
            self,
            user_id: int,
    ) -> None:
        """
        Delete a user.
        """

        db_obj = self.repository.get(user_id)

        if db_obj is None:
            raise NotFoundError(
                "User not found."
            )

        self.repository.delete(db_obj)
