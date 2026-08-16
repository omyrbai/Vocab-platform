import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from argon2.exceptions import InvalidHashError

from app.core.settings import settings
from app.enums.token_type import TokenType


_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a password using Argon2id.
    """

    return _password_hasher.hash(password)


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Verify a password against an Argon2id hash.
    """

    try:
        return _password_hasher.verify(
            password_hash,
            password,
        )
    except (
        VerificationError,
        InvalidHashError,
    ):
        return False


def _load_private_key() -> str:
    """
    Load the RSA private key used to sign JWTs.
    """

    return Path(
        settings.JWT_PRIVATE_KEY_PATH
    ).read_text(
        encoding="utf-8",
    )


def _load_public_key() -> str:
    """
    Load the RSA public key used to verify JWTs.
    """

    return Path(
        settings.JWT_PUBLIC_KEY_PATH
    ).read_text(
        encoding="utf-8",
    )


def create_access_token(
    user_id: int,
) -> str:
    """
    Create a short-lived JWT access token.
    """

    now = datetime.now(timezone.utc)
    expires_at = (
        now
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    )

    payload = {
        "sub": str(user_id),
        "type": TokenType.ACCESS.value,
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        _load_private_key(),
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict:
    """
    Decode and verify a JWT access token.
    """

    return jwt.decode(
        token,
        _load_public_key(),
        algorithms=[settings.JWT_ALGORITHM],
    )


def generate_refresh_token() -> str:
    """
    Generate a cryptographically secure refresh token.
    """

    return secrets.token_urlsafe(64)


def hash_refresh_token(
    refresh_token: str,
) -> str:
    """
    Hash a refresh token before storing it.
    """

    return hashlib.sha256(
        refresh_token.encode("utf-8")
    ).hexdigest()