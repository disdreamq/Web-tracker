"""
FastAPI dependencies for JWT authentication and authorization.
"""

from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from src.api.v1.auth.schemas import TokenData
from src.core.config import get_settings
from src.core.exceptions.http import AuthenticationException
from src.dependencies import get_user_service
from src.user.schemas import SUserDTO
from src.user.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def require_auth(
    service: Annotated[UserService, Depends(get_user_service)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> SUserDTO:
    """
    Dependency for authenticating and authorizing requests with JWT.

    Extracts JWT token from Authorization header, decodes and validates it,
    then retrieves the corresponding user from the database.

    Args:
        service: User service instance for database operations.
        token: JWT access token extracted from Authorization header.

    Returns:
        SUserDTO: Authenticated user data.

    Raises:
        AuthenticationException: If token is invalid, expired, or user not found.
    """
    secret_key = get_settings().secret_key
    algorithm = get_settings().alghoritm
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username = payload.get("sub")
        if username is None:
            raise AuthenticationException("Auth error") from None
        token_data = TokenData(username=username)
        if not token_data.username:
            raise AuthenticationException("Auth error") from None
    except InvalidTokenError:
        raise AuthenticationException("Auth error") from None

    user = await service.get_by_email(token_data.username)
    if user is None:
        raise AuthenticationException("Auth error") from None
    return SUserDTO.model_validate(user)
