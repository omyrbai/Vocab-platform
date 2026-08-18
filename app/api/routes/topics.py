from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.exceptions import ConflictError, NotFoundError
from app.api.dependencies import get_db
from app.dependencies import get_topic_service
from app.schemas.topic import TopicRead, TopicCreate, TopicUpdate

router = APIRouter(
    prefix="/api/v1/topics",
    tags=["Topics"],
)

@router.get(
    "/",
    response_model=list[TopicRead],
)
def get_topics(
    session: Session = Depends(get_db),
):
    topic_service = get_topic_service(session)

    return topic_service.get_all()

@router.get(
    "/{topic_id}",
    response_model=TopicRead,
)
def get_topic(
    topic_id: int,
    session: Session = Depends(get_db),
):
    topic_service = get_topic_service(session)

    topic = topic_service.get(topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found.",
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
):
    topic_service = get_topic_service(session)

    try:
        return topic_service.create(create_data)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

@router.patch(
    "/{topic_id}",
    response_model=TopicRead,
)
def update_topic(
    topic_id: int,
    update_data: TopicUpdate,
    session: Session = Depends(get_db),
):
    topic_service = get_topic_service(session)

    topic = topic_service.get(topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found."
        )

    try:
        return topic_service.update(
            topic,
            update_data,
        )

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

@router.delete(
    "/{topic_id}",
    status_code=204,
)
def delete_topic(
    topic_id: int,
    session: Session = Depends(get_db),
):
    topic_service = get_topic_service(session)

    topic = topic_service.get(topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found.",
        )

    topic_service.delete(topic)