from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base_model.base import Base


class User(Base):
    """
    Database model for users.

    Attributes:
        id: Primary key.
        email: User email (unique).
        password: User password hash.
        tracking_sites: List of tracked site URLs.
        created_at: Timestamp of user creation.
        updated_at: Timestamp of last update.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    tracking_sites: Mapped[str] = mapped_column(default="[]")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
