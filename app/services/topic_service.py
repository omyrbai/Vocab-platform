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
        user_id: int | None,
        topic_id: int,
    ) -> Topic | None:
        """
        Get a topic.

        If user_id is provided, the topic must belong
        to that user. If user_id is None, return the
        topic regardless of owner.
        """
        if user_id is None:
            return self.repository.get(topic_id)

        return self.repository.get_by_id_for_user(
            topic_id=topic_id,
            user_id=user_id,
        )

    def get_by_name(
        self,
        user_id: int,
        name: str,
    ) -> Topic | None:
        """
        Get a topic by name.
        """
        return self.repository.get_by_name(
            user_id=user_id,
            name=name,
        )

    def get_by_parent_and_name(
            self,
            user_id: int,
            parent_topic_id: int | None,
            name: str,
    ) -> Topic | None:
        """
        Get a topic by parent topic ID and name.
        """
        return self.repository.get_by_parent_and_name(
            user_id=user_id,
            parent_topic_id=parent_topic_id,
            name=name,
        )

    def get_all(
        self,
        user_id: int | None = None,
    ) -> Sequence[Topic]:
        """
        Get all topics.

        If user_id is provided, return only that user's topics.
        If user_id is None, return all topics.
        """

        return self.repository.get_all(
            user_id=user_id,
        )

    def create(
            self,
            user_id: int,
            create_data: TopicCreate,
            *,
            is_admin: bool = False,
            commit: bool = True,
    ) -> Topic:
        """
        Create a new topic.

        If a parent topic is provided, the new topic belongs
        to the same user as the parent topic.
        """

        owner_id = user_id

        if create_data.parent_topic_id is not None:
            parent_topic = self.get(
                user_id=None if is_admin else user_id,
                topic_id=create_data.parent_topic_id,
            )

            if parent_topic is None:
                raise NotFoundError(
                    "Parent topic not found."
                )

            owner_id = parent_topic.user_id

        existing_topic = self.get_by_parent_and_name(
            user_id=owner_id,
            parent_topic_id=create_data.parent_topic_id,
            name=create_data.name,
        )

        if existing_topic is not None:
            raise ConflictError(
                "Topic already exists under this particular parent."
            )

        return self.repository.create_for_user(
            user_id=owner_id,
            create_data=create_data,
            commit=commit,
        )

    def update(
        self,
        user_id: int | None,
        db_obj: Topic,
        update_data: TopicUpdate,
    ) -> Topic:
        """
        Update a topic owned by the specified user.
        """

        if (
            user_id is not None
            and db_obj.user_id != user_id
        ):
            raise NotFoundError(
                "Topic not found."
            )

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
            parent_topic = self.get(
                user_id=None,
                topic_id=parent_topic_id,
            )

            if (
                    parent_topic is None
                    or parent_topic.user_id != db_obj.user_id
            ):
                raise NotFoundError(
                    "Parent topic not found."
                )

        if parent_topic_id == db_obj.topic_id:
            raise ConflictError(
                "A topic cannot be its own parent."
            )

        existing_topic = self.find_duplicate(
            user_id=db_obj.user_id,
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
        user_id: int | None,
        db_obj: Topic,
    ) -> None:
        """
        Delete a topic owned by the specified user.
        """
        if (
            user_id is not None
            and db_obj.user_id != user_id
        ):
            raise NotFoundError(
                "Topic not found."
            )
        self.repository.delete(db_obj)

    def find_duplicate(
        self,
        user_id: int,
        parent_topic_id: int | None,
        name: str,
        exclude_topic_id: int | None,
    ) -> Topic | None:
        """
        Find a topic under the same parent.
        """

        return self.repository.find_duplicate(
            user_id=user_id,
            parent_topic_id=parent_topic_id,
            name=name,
            exclude_topic_id=exclude_topic_id,
        )
