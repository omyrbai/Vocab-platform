from collections.abc import Sequence

from app.db.models.topic import Topic
from app.exceptions import ConflictError, NotFoundError
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

    def get_by_parent_and_name(
            self,
            parent_topic_id: int | None,
            name: str,
    ) -> Topic | None:
        """
        Get a topic by parent topic ID and name.
        """
        return self.repository.get_by_parent_and_name(
            parent_topic_id=parent_topic_id,
            name=name,
        )

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

        if create_data.parent_topic_id is not None:
            parent_topic = self.get(
                create_data.parent_topic_id,
            )

            if parent_topic is None:
                raise NotFoundError(
                    "Parent topic not found."
                )

        existing_topic = self.get_by_parent_and_name(
            parent_topic_id=create_data.parent_topic_id,
            name=create_data.name,
        )

        if existing_topic is not None:
            raise ConflictError(
                "Topic already exists under this particular parent."
            )

        return self.repository.create(create_data)

    def update(
            self,
            db_obj: Topic,
            update_data: TopicUpdate,
    ) -> Topic:
        """
        Update a topic.
        """

        parent_topic_id = (
            update_data.parent_topic_id
            if update_data.parent_topic_id is not None
            else db_obj.parent_topic_id
        )

        name = (
            update_data.name
            if update_data.name is not None
            else db_obj.name
        )

        if parent_topic_id is not None:
            parent_topic = self.get(parent_topic_id)

            if parent_topic is None:
                raise NotFoundError(
                    "Parent topic not found."
                )
        if parent_topic_id == db_obj.topic_id:
            raise ConflictError(
                "A topic cannot be its own parent."
            )

        existing_topic = self.find_duplicate(
            parent_topic_id=parent_topic_id,
            name=name,
            exclude_topic_id=db_obj.topic_id,
        )

        if existing_topic is not None:
            raise ConflictError(
                "Topic already exists under this particular parent."
            )

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

    def find_duplicate(
        self,
        parent_topic_id: int | None,
        name: str,
        exclude_topic_id: int | None,
    ) -> Topic | None:
        """
        Find a topic under the same parent.
        """

        return self.repository.find_duplicate(
            parent_topic_id=parent_topic_id,
            name=name,
            exclude_topic_id=exclude_topic_id,
        )
