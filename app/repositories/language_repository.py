from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.language import Language
from app.repositories.base_repository import BaseRepository
from app.schemas.language import (
    LanguageCreate,
    LanguageUpdate,
)


class LanguageRepository(
    BaseRepository[
        Language,
        LanguageCreate,
        LanguageUpdate,
    ]
):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session=session,
            model=Language,
            pk_field="lang_id",
        )

    def get_by_code(
            self,
            lang_code: str,
    ) -> Language | None:
        """
        Get a language by code.
        """

        stmt = (
            select(self.model)
            .where(self.model.lang_code == lang_code)
        )

        return self.session.scalar(stmt)

    def get_all(
            self,
    ) -> Sequence[Language]:
        """
        Get all languages.
        """

        stmt = (
            select(self.model)
            .order_by(self.model.language_name)
        )

        return self.session.scalars(stmt).all()
