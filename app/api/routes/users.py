from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.dependencies import get_user_service
from app.exceptions import ConflictError, NotFoundError
from app.schemas.user import (
    UserRead,
    UserCreate,
    UserUpdate
)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserRead],
)
def get_users(
    session: Session = Depends(get_db),
):
    user_service = get_user_service(session)

    return user_service.get_all()

@router.get(
    "/{user_id}",
    response_model=UserRead,
)
def get_user(
    user_id: int,
    session: Session = Depends(get_db),
):
    user_service = get_user_service(session)

    user = user_service.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user

@router.post(
    "/",
    response_model=UserRead,
    status_code=201,
)
def create_user(
    create_data: UserCreate,
    session: Session = Depends(get_db),
):
    user_service = get_user_service(session)

    try:
        return user_service.create(create_data)

    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.patch(
    "/{user_id}",
    response_model=UserRead,
)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    session: Session = Depends(get_db),
):
    user_service = get_user_service(session)

    try:
        return user_service.update(
            user_id,
            update_data,
        )

    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.delete(
    "/{user_id}",
    status_code=204,
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_db),
):
    user_service = get_user_service(session)

    try:
        user_service.delete(user_id)

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )