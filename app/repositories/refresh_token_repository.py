from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.refresh_token import RefreshToken
from app.repositories.base_repository import BaseRepository
from app.schemas.refresh_token import RefreshTokenCreate

class RefreshTokenRepository(
    BaseRepository[
        RefreshToken,
        RefreshTokenCreate,
        RefreshTokenCreate,
    ]
):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session=session,
            model=RefreshToken,
            pk_field="refresh_token_id",
        )

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        stmt = (
            select(self.model)
            .where(
                self.model.token_hash == token_hash,
            )
        )

        return self.session.scalar(stmt)

    def get_active_by_token_hash(
        self,
        token_hash: str,
        now: datetime,
    ) -> RefreshToken | None:
        stmt = (
            select(self.model)
            .where(
                self.model.token_hash == token_hash,
                self.model.revoked_at.is_(None),
                self.model.expires_at > now,
            )
        )

        return self.session.scalar(stmt)

    def revoke(
            self,
            db_obj: RefreshToken,
    ) -> None:
        """
        Revoke a refresh token without committing.
        """

        db_obj.revoked_at = datetime.now(timezone.utc)

        self.session.flush()