"""
Authentication service for user login and token management.
"""

from typing import Annotated

from fastapi import Depends

from src.api.v1.auth.schemas import STokenResponse
from src.core.exceptions.http import AuthenticationException
from src.core.security.security import verify_password
from src.dependencies import get_user_service
from src.user.schemas import SUserDTO
from src.user.service import UserService


async def authenticate_user(
    service: Annotated[UserService, Depends(get_user_service)],
    email: str,
    password: str,
) -> SUserDTO:
    """
    Authenticate a user by email and password.

    Retrieves user by email and verifies password hash.

    Args:
        service: User service instance for database operations.
        email: User email address.
        password: Plain text password.

    Returns:
        SUserDTO: Authenticated user data.

    Raises:
        AuthenticationException: If user not found or password invalid.
    """
    user = await service.get_by_email(email)
    if not user or not verify_password(
        plain_password=password, hash_password=user.password
    ):
        raise AuthenticationException(
            f"Can not authenticate user with {email=} and {password=}"
        )
    return SUserDTO.model_validate(user)


def create_token_response(access_token: str) -> STokenResponse:
    """
    Create a token response object for API response.

    Args:
        access_token: JWT access token string.

    Returns:
        STokenResponse: Token response with access_token and token_type.
    """
    return STokenResponse(access_token=access_token, token_type="bearer")
