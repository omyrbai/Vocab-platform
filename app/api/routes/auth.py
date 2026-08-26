from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.schemas.user import (
    UserRead,
    UserUpdate,
)
from app.dependencies import (
    get_auth_service,
    get_user_service,
)

from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

@router.get(
    "/me",
    response_model=UserRead,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.patch(
    "/me",
    response_model=UserRead,
)
def update_me(
    update_data: UserUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = get_user_service(session)

    return user_service.update(
        current_user.user_id,
        update_data,
    )

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=201,
)
def register(
    register_data: RegisterRequest,
    session: Session = Depends(get_db),
):
    auth_service = get_auth_service(session)

    return auth_service.register(
        register_data,
    )

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    session: Session = Depends(get_db),
):
    auth_service = get_auth_service(session)


    return auth_service.login(
        identifier=login_data.identifier,
        password=login_data.password,
    )

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    refresh_data: RefreshRequest,
    session: Session = Depends(get_db),
):
    auth_service = get_auth_service(session)

    return auth_service.refresh(
        refresh_data.refresh_token,
    )

@router.post(
    "/logout",
    status_code=204,
)
def logout(
    refresh_data: RefreshRequest,
    session: Session = Depends(get_db),
):
    auth_service = get_auth_service(session)

    auth_service.logout(
        refresh_data.refresh_token,
    )