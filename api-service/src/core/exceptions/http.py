from typing import Any

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        detail: str | None = None,
        headers: dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status_code, detail=detail or message, headers=headers
        )
        self.message = message


class ValidationException(BaseHTTPException):
    def __init__(self, message: str, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            detail=detail,
        )


class AuthenticationException(BaseHTTPException):
    def __init__(self, message: str, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
