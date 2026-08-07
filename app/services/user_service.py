from collections.abc import Sequence

from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserService:

    def __init__(
            self,
            repository: UserRepository,
    ):
        self.repository = repository

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
                raise ValueError(
                    "Telegram user already exists."
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
            raise ValueError(
                "User not found."
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
            raise ValueError(
                "User not found."
            )

        self.repository.delete(db_obj)
