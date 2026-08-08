from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.topic import Topic
from app.repositories.base_repository import BaseRepository
from app.schemas.topic import (
    TopicCreate,
    TopicUpdate,
)


class TopicRepository(
    BaseRepository[
        Topic,
        TopicCreate,
        TopicUpdate,
    ]
):
    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session=session,
            model=Topic,
            pk_field="topic_id",
        )

    def get_by_name(
            self,
            name: str,
    ) -> Topic | None:
        """
        Get a topic by name.
        """

        stmt = (
            select(self.model)
            .where(self.model.name == name)
        )

        return self.session.scalar(stmt)

    def get_by_parent_and_name(
        self,
        parent_topic_id: int | None,
        name: str,
    ) -> Topic | None:
        """
        Get a topic by parent topic ID and  name.
        """
        stmt = (
            select(self.model)
            .where(
                self.model.parent_topic_id == parent_topic_id,
                self.model.name == name,
            )
        )

        return self.session.scalar(stmt)

    def get_all(
            self,
    ) -> Sequence[Topic]:
        """
        Get all topics.
        """

        stmt = (
            select(self.model)
            .order_by(self.model.name)
        )

        return self.session.scalars(stmt).all()
