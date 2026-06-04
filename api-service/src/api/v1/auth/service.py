from typing import Annotated

from fastapi import Depends

from src.api.v1.auth.schemas import STokenResponse
from src.core.exceptions.http import AuthenticationException
from src.core.security import verify_password
from src.dependencies import get_user_service
from src.user.schemas import SUserDTO
from src.user.service import UserService


async def authenticate_user(
    service: Annotated[UserService, Depends(get_user_service)],
    email: str,
    password: str,
) -> SUserDTO:
    user = await service.get_by_email(email)
    if not user or not verify_password(
        plain_password=password, hash_password=user.password
    ):
        raise AuthenticationException(
            f"Can not authenticate user with {email=} and {password=}"
        )
    return SUserDTO.model_validate(user)


def create_token_response(access_token: str) -> STokenResponse:
    return STokenResponse(access_token=access_token, token_type="bearer")
