"""
Security Utilities

This module contains security-related utility functions for the application,
including password hashing, JWT creation, and token decoding.

Key Components:
- pwd_context: A Passlib context for hashing and verifying passwords using bcrypt.
- create_access_token: Generates a JWT for a given user identity.
- decode_access_token: Decodes and validates a JWT, returning the payload.
- get_password_hash: Hashes a plain-text password.
- verify_password: Verifies a plain-text password against its hash.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

# --- Password Hashing Setup ---
# We use bcrypt as the hashing scheme. It's a strong, widely-used algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.

    Args:
        plain_password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using the configured scheme (bcrypt).

    Args:
        password (str): The password to hash.

    Returns:
        str: The resulting hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Creates a new JWT access token.

    The token's expiration time is determined by the `ACCESS_TOKEN_EXPIRE_MINUTES`
    setting in the application's configuration.

    Args:
        data (Dict[str, Any]): The payload to encode into the token. Typically
                               contains user identification information like 'sub'.

    Returns:
        str: The encoded JWT as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and validates a JWT access token.

    Args:
        token (str): The JWT to decode.

    Returns:
        Optional[Dict[str, Any]]: The token's payload if validation is successful,
                                  otherwise None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        # This will catch any validation error, including expired tokens,
        # invalid signatures, etc.
        return None