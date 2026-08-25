from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.schemas.user import (
    UserRead,
)
from app.dependencies import get_auth_service

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
        email=login_data.email,
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