from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.enums.user_role import UserRole
from app.exceptions import NotFoundError
from app.dependencies import get_topic_service
from app.schemas.topic import TopicRead, TopicCreate, TopicUpdate

router = APIRouter(
    prefix="/api/v1/topics",
    tags=["Topics"],
)

def get_topic_user_id(
    current_user: User,
) -> int | None:
    if current_user.role == UserRole.ADMIN:
        return None

    return current_user.user_id

@router.get(
    "/",
    response_model=list[TopicRead],
)
def get_topics(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic_service = get_topic_service(session)

    return topic_service.get_all(
        user_id=get_topic_user_id(current_user),
    )

@router.get(
    "/{topic_id}",
    response_model=TopicRead,
)
def get_topic(
    topic_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic_service = get_topic_service(session)

    topic = topic_service.get(
        user_id=get_topic_user_id(current_user),
        topic_id=topic_id,
    )

    if topic is None:
        raise NotFoundError(
            "Topic not found."
        )

    return topic

@router.post(
    "/",
    response_model=TopicRead,
    status_code=201,
)
def create_topic(
    create_data: TopicCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic_service = get_topic_service(session)

    return topic_service.create(
        user_id=current_user.user_id,
        create_data=create_data
    )


@router.patch(
    "/{topic_id}",
    response_model=TopicRead,
)
def update_topic(
    topic_id: int,
    update_data: TopicUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic_service = get_topic_service(session)

    topic = topic_service.get(
        user_id=get_topic_user_id(current_user),
        topic_id=topic_id,
    )

    if topic is None:
        raise NotFoundError(
            "Topic not found."
        )


    return topic_service.update(
        user_id=get_topic_user_id(current_user),
        db_obj=topic,
        update_data=update_data,
    )

@router.delete(
    "/{topic_id}",
    status_code=204,
)
def delete_topic(
    topic_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    topic_service = get_topic_service(session)

    topic = topic_service.get(
        user_id=get_topic_user_id(current_user),
        topic_id=topic_id,
    )

    if topic is None:
        raise NotFoundError(
            "Topic not found."
        )

    topic_service.delete(
        user_id=get_topic_user_id(current_user),
        db_obj=topic,
    )