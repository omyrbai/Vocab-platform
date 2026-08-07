from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.base_repository import BaseRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserRepository(
    BaseRepository[
        User,
        UserCreate,
        UserUpdate,
    ]
):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session=session,
            model=User,
            pk_field="user_id",
        )

    def get_by_telegram_id(
            self,
            telegram_id: int,
    ) -> User | None:
        """
        Get a user by telegram id.
        """

        stmt = (
            select(self.model)
            .where(self.model.telegram_id == telegram_id)
        )

        return self.session.scalar(stmt)

    def get_all(
            self,
    ) -> Sequence[User]:
        """
        Get all users.
        """

        stmt = (
            select(self.model)
            .order_by(
                self.model.first_name,
                self.model.user_id,
            )
        )

        return self.session.scalars(stmt).all()

    def get_by_username(
            self,
            username: str,
    ) -> User | None:
        """
        Get a user by username.
        """
        stmt = (
            select(self.model)
            .where(
                self.model.username == username,
            )
        )

        return self.session.scalar(stmt)