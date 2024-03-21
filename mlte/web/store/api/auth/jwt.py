"""
mlte/web/store/api/auth/jwt.py

Handling of JWT tokens.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt

from mlte.model.base_model import BaseModel

SECRET_KEY = "399fd92f61c99e35d7f2f6fdb9d65293c4047f9ac500af1886b8868b495f20b3"
"""Used for signing tokens."""

ALGORITHM = "HS256"
"""Token hashing algorithm."""

DEFAULT_EXPIRATION_MINS = 30
"""Default token expiration time."""

SUBJECT_CLAIM_KEY = "sub"
EXPIRATION_CLAIM_KEY = "exp"
"""Token claim keys."""


class Token(BaseModel):
    """Model for the token."""

    encoded_token: str
    """The actual encoded token."""

    expires_in: int
    """Lifetime in seconds of the token."""


def create_user_token(username: str) -> Token:
    """Creates an access token containing a given username."""
    data = {SUBJECT_CLAIM_KEY: username}
    access_token = _create_access_token(data)
    return access_token


def _create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
) -> Token:
    """Creates a token given a data dictionary and an expiration time."""
    claims = data.copy()

    # Calculate expiration time, and add it to claims.
    if expires_delta is None:
        expires_delta = timedelta(minutes=DEFAULT_EXPIRATION_MINS)
    expiration_time = datetime.now(timezone.utc) + expires_delta
    claims.update({EXPIRATION_CLAIM_KEY: expiration_time})

    # Encode and sign token, and return it.
    encoded_jwt = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    token = Token(
        encoded_token=encoded_jwt, expires_in=int(expires_delta.total_seconds())
    )
    return token


def decode_user_token(encoded_token: str) -> str:
    """Decodes the provided user access token."""
    try:
        payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get(SUBJECT_CLAIM_KEY)
        if username is None:
            raise Exception("No valid user in token")
        return username
    except JWTError as ex:
        raise Exception(f"Error decoding token: {str(ex)}")
