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

    def create_for_user(
        self,
        user_id: int,
        create_data: TopicCreate,
        *,
        commit: bool = True,
    ) -> Topic:
        """
        Create a new topic.
        """

        topic = Topic(
            user_id=user_id,
            parent_topic_id=create_data.parent_topic_id,
            name=create_data.name,
            description=create_data.description,
        )

        self.session.add(topic)
        self.session.flush()

        if commit:
            self.session.commit()
            self.session.refresh(topic)

        return topic

    def get_by_id_for_user(
            self,
            topic_id: int,
            user_id: int,
    ) -> Topic | None:
        stmt = (
            select(self.model)
            .where(
                self.model.topic_id == topic_id,
                self.model.user_id == user_id,
            )
        )

        return self.session.scalar(stmt)

    def get_by_name(
            self,
            user_id: int,
            name: str,
    ) -> Topic | None:
        """
        Get a topic by name.
        """

        stmt = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.name == name,
            )
        )

        return self.session.scalar(stmt)

    def get_by_parent_and_name(
        self,
        user_id: int,
        parent_topic_id: int | None,
        name: str,
    ) -> Topic | None:
        """
        Get a topic by parent topic ID and  name.
        """
        stmt = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.parent_topic_id == parent_topic_id,
                self.model.name == name,
            )
        )

        return self.session.scalar(stmt)

    def get_all(
        self,
        user_id: int | None = None,
    ) -> Sequence[Topic]:
        """
        Get topics.

        If user_id is provided, return only that user's topics.
        If user_id is None, return all topics.
        """
        stmt = select(self.model)

        if user_id is not None:
            stmt = stmt.where(
                self.model.user_id == user_id
            )

        stmt = stmt.order_by(self.model.name)


        return self.session.scalars(stmt).all()

    def find_duplicate(
            self,
            user_id: int,
            parent_topic_id: int | None,
            name: str,
            exclude_topic_id: int | None,
    ) -> Topic | None:
        """
        Find a topic with the same parent and name, excluding a specific topic if provided.
        """

        stmt = (
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.parent_topic_id == parent_topic_id,
                self.model.name == name,
            )
        )

        if exclude_topic_id is not None:
            stmt = stmt.where(
                self.model.topic_id != exclude_topic_id
            )

        return self.session.scalar(stmt)