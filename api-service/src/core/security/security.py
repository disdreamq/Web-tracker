"""
Security utilities for password hashing and JWT token handling.
"""

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from src.core.config import get_settings

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using the recommended algorithm.

    Args:
        password: Plain text password to hash.

    Returns:
        Hashed password string.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    """
    Verify a plain text password against its hash.

    Args:
        plain_password: Plain text password to verify.
        hash_password: Hashed password to compare against.

    Returns:
        True if password matches, False otherwise.
    """
    return password_hash.verify(password=plain_password, hash=hash_password)


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=15)
) -> str:
    """
    Create a JWT access token with expiration.

    Args:
        data: Payload data to encode (typically contains user identifier).
        expires_delta: Token expiration time delta. Defaults to 15 minutes.

    Returns:
        Encoded JWT token string.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().secret_key,
        algorithm=get_settings().alghoritm,
    )
    return encoded_jwt
