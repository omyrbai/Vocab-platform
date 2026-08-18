from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user_identity import UserIdentity
from app.enums.auth_provider import AuthProvider
from app.repositories.base_repository import BaseRepository
from app.schemas.user_identity import UserIdentityCreate


class UserIdentityRepository(
    BaseRepository[
        UserIdentity,
        UserIdentityCreate,
        UserIdentityCreate,
    ]
):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session=session,
            model=UserIdentity,
            pk_field="identity_id",
        )

    def get_by_provider_user_id(
        self,
        provider: AuthProvider,
        provider_user_id: str,
    ) -> UserIdentity | None:
        stmt = (
            select(self.model)
            .where(
                self.model.provider == provider.value,
                self.model.provider_user_id == provider_user_id,
            )
        )

        return self.session.scalar(stmt)

    def get_by_email(
        self,
        email: str,
    ) -> UserIdentity | None:
        stmt = (
            select(self.model)
            .where(
                self.model.provider == AuthProvider.EMAIL.value,
                self.model.email == email,
            )
        )

        return self.session.scalar(stmt)

    def get_by_user_id(
        self,
        user_id: int,
    ) -> Sequence[UserIdentity]:
        stmt = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
            )
            .order_by(self.model.identity_id)
        )

        return self.session.scalars(stmt).all()