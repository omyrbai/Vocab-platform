from collections.abc import Sequence

from app.db.models.topic import Topic
from app.repositories.topic_repository import TopicRepository
from app.schemas.topic import (
    TopicCreate,
    TopicUpdate,
)


class TopicService:

    def __init__(
            self,
            repository: TopicRepository,
    ):
        self.repository = repository

    def get(
            self,
            topic_id: int,
    ) -> Topic | None:
        """
        Get a topic by ID.
        """
        return self.repository.get(topic_id)

    def get_by_name(
            self,
            name: str,
    ) -> Topic | None:
        """
        Get a topic by name.
        """
        return self.repository.get_by_name(name)

    def get_all(
            self,
    ) -> Sequence[Topic]:
        """
        Get all topics.
        """
        return self.repository.get_all()

    def create(
            self,
            create_data: TopicCreate,
    ) -> Topic:
        """
        Create a new topic.
        """
        return self.repository.create(create_data)

    def update(
            self,
            db_obj: Topic,
            update_data: TopicUpdate,
    ) -> Topic:
        """
        Update a topic.
        """
        return self.repository.update(
            db_obj,
            update_data,
        )

    def delete(
            self,
            db_obj: Topic,
    ) -> None:
        """
        Delete a topic.
        """
        self.repository.delete(db_obj)
