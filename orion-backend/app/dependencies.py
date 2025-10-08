"""
Application-Wide Dependencies

This module defines common dependencies used across different API routers
in the application. These dependencies help to encapsulate and reuse logic
for tasks like authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core import security
from app.modules.auth import service as auth_service, schemas as auth_schemas

# --- Authentication Dependency ---

# This scheme defines that the token should be sent in the Authorization header
# as a Bearer token. The tokenUrl points to the login endpoint.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> auth_schemas.UserPublic:
    """
    Dependency to get the current authenticated user.

    This function decodes the JWT from the request's Authorization header,
    validates it, and fetches the corresponding user from the database.

    Args:
        token (str): The OAuth2 bearer token.
        db (Session): The database session.

    Raises:
        HTTPException(401): If the token is invalid, expired, or the user
                            is not found.

    Returns:
        auth_schemas.UserPublic: The authenticated user's public data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = security.decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = auth_service.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    return user