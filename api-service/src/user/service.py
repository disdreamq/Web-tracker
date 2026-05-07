import logging

from src.user.repository import SQLAlchemyUserRepository
from src.user.schemas import UserCreate, UserDTO, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    """
    Service for managing users (CRUD operations).

    Provides business logic for user operations:
    - Create, Read, Update, Delete
    - Email uniqueness validation
    - Entity to DTO transformation

    Attributes:
        repo: Repository for database access.
    """

    def __init__(self, repo: SQLAlchemyUserRepository):
        """
        Initialize service with repository.

        Args:
            repo: Repository for data access.
        """
        self.repo = repo

    async def create(self, user_to_create: UserCreate) -> UserDTO:
        """
        Create a new user record in the database.

        Checks email uniqueness before creating.

        Args:
            user_to_create: Data for creating the user.

        Returns:
            DTO of the created user.

        Raises:
            ValueError: If a user with this email already exists.
        """
        if await self.repo.get_by_email(user_to_create.email):
            logger.exception(
                f"Email already exists during create user: email={user_to_create.email}"
            )
            raise ValueError(
                f"Cannot add user to database, email already exists: {user_to_create.email=}"  # noqa: E501
            )

        user_in_db = await self.repo.create(
            email=str(user_to_create.email),
            password=user_to_create.password,
            tracking_sites=user_to_create.tracking_sites,
        )
        logger.info(f"Added user to database: email = {user_to_create.email}")
        return UserDTO.model_validate(user_in_db)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """
        Get a user by email.

        Args:
            email: User email.

        Returns:
            User DTO or None if not found.
        """
        if user := await self.repo.get_by_email(email):
            return UserDTO.model_validate(user)
        return None

    async def get_by_id(self, id: int) -> UserDTO | None:
        """
        Get a user by ID.

        Args:
            id: User ID.

        Returns:
            User DTO or None if not found.
        """
        if user := await self.repo.get_by_id(id):
            return UserDTO.model_validate(user)
        return None

    async def update(self, id: int, user_update: UserUpdate) -> UserDTO | None:
        """
        Update user fields.

        Args:
            id: User ID.
            user_update: Fields to update.

        Returns:
            DTO of the updated user or None if not found.
        """
        update_data = user_update.model_dump(exclude_unset=True)
        if update_data:
            if await self.repo.get_by_email(update_data["email"]) and update_data.get(
                "email"
            ):
                logger.exception(
                    f"Email already exists during update user: id={id}, email={update_data.get('email')}"  # noqa: E501
                )
                raise ValueError(
                    f"Cannot update user, email already exists: {update_data.get('email')=}"  # noqa: E501
                )

            user_in_db = await self.repo.update(id=id, **update_data)
            if user_in_db:
                logger.info(f"Updated user in database: id = {id}")
                return UserDTO.model_validate(user_in_db)
        return None

    async def delete(self, id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            id: User ID.

        Returns:
            True if deleted, False if not found.
        """
        logger.info(f"Deleted user from database: id={id}")
        return await self.repo.delete(id)
