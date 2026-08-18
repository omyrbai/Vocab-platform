from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)

from app.core.settings import settings
from app.enums.auth_provider import AuthProvider
from app.exceptions import ConflictError
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_identity_repository import UserIdentityRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
)
from app.schemas.refresh_token import RefreshTokenCreate
from app.schemas.user import UserCreate
from app.schemas.user_identity import UserIdentityCreate


class AuthService:

    def __init__(
        self,
        session: Session,
        user_repository: UserRepository,
        identity_repository: UserIdentityRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.session = session
        self.user_repository = user_repository
        self.identity_repository = identity_repository
        self.refresh_token_repository = refresh_token_repository

    def register(
            self,
            register_data: RegisterRequest,
    ) -> TokenResponse:
        """
        Register a new user and issue authentication tokens.
        """

        email = register_data.email.lower()

        existing_identity = (
            self.identity_repository.get_by_email(email)
        )

        if existing_identity is not None:
            raise ConflictError(
                "Email already exists."
            )

        try:
            user = self.user_repository.create(
                UserCreate(
                    first_name=register_data.first_name,
                ),
                commit=False,
            )

            self.identity_repository.create(
                UserIdentityCreate(
                    user_id=user.user_id,
                    provider=AuthProvider.EMAIL,
                    provider_user_id=email,
                    email=email,
                    password_hash=hash_password(
                        register_data.password
                    ),
                ),
                commit=False,
            )

            refresh_token = generate_refresh_token()

            refresh_token_hash = hash_refresh_token(
                refresh_token,
            )

            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(
                    days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
                )
            )

            self.refresh_token_repository.create(
                RefreshTokenCreate(
                    user_id=user.user_id,
                    token_hash=refresh_token_hash,
                    expires_at=expires_at,
                ),
                commit=False,
            )

            access_token = create_access_token(
                user.user_id,
            )

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def login(
            self,
            email: str,
            password: str,
    ) -> TokenResponse:
        """
        Authenticate a user using email and password.
        """

        email = email.lower()

        identity = self.identity_repository.get_by_email(
            email,
        )

        if (
                identity is None
                or identity.password_hash is None
                or not verify_password(
            password,
            identity.password_hash,
        )
        ):
            raise ValueError(
                "Invalid email or password."
            )

        refresh_token = generate_refresh_token()

        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        expires_at = (
            datetime.now(timezone.utc)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            )
        )

        try:
            self.refresh_token_repository.create(
                RefreshTokenCreate(
                    user_id=identity.user_id,
                    token_hash=refresh_token_hash,
                    expires_at=expires_at,
                ),
                commit=False,
            )

            access_token = create_access_token(
                identity.user_id,
            )

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh(
            self,
            refresh_token: str,
    ) -> TokenResponse:
        """
        Rotate a refresh token and issue new tokens.
        """

        token_hash = hash_refresh_token(
            refresh_token,
        )

        now = datetime.now(timezone.utc)
        db_token = (
            self.refresh_token_repository
            .get_active_by_token_hash(
                token_hash,
                now,
            )
        )

        if db_token is None:
            raise ValueError(
                "Invalid refresh token."
            )

        try:
            self.refresh_token_repository.revoke(
                db_token,
            )

            new_refresh_token = generate_refresh_token()

            new_refresh_token_hash = hash_refresh_token(
                new_refresh_token,
            )

            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(
                    days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
                )
            )

            self.refresh_token_repository.create(
                RefreshTokenCreate(
                    user_id=db_token.user_id,
                    token_hash=new_refresh_token_hash,
                    expires_at=expires_at,
                ),
                commit=False,
            )

            access_token = create_access_token(
                db_token.user_id,
            )

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    def logout(
            self,
            refresh_token: str,
    ) -> None:
        """
        Revoke a refresh token.
        """

        token_hash = hash_refresh_token(
            refresh_token,
        )

        db_token = (
            self.refresh_token_repository
            .get_by_token_hash(token_hash)
        )

        if db_token is None:
            return

        if db_token.revoked_at is not None:
            return

        try:
            self.refresh_token_repository.revoke(
                db_token,
            )

            self.session.commit()

        except Exception:
            self.session.rollback()
            raise