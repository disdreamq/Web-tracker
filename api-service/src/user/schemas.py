from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email: User email (validated EmailStr).
        password: User password.
        tracking_sites: List of tracked site URLs.
    """

    email: EmailStr
    password: str
    tracking_sites: list[str] = []


class UserUpdate(BaseModel):
    """
    Schema for updating a user.

    Attributes:
        email: New user email (optional).
        password: New user password (optional).
        tracking_sites: New list of tracked site URLs (optional).
    """

    email: EmailStr | None = None
    password: str | None = None
    tracking_sites: list[str] | None = None


class UserDTO(BaseModel):
    """
    Data Transfer Object for user entity.

    Attributes:
        id: Unique identifier of the user.
        email: User email.
        tracking_sites: List of tracked site URLs.
        created_at: Timestamp of user creation.
        updated_at: Timestamp of last update.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    tracking_sites: list[str]
