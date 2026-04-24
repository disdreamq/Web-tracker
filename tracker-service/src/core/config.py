import logging
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)
load_dotenv(Path(__file__).resolve().parents[3] / ".env")


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Configuration for:
    - Logging
    - PostgreSQL database
    - Redis cache

    Attributes:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_format: Logging format string.
        postgres_db: Database name.
        postgres_host: Database host address.
        postgres_port: Database port.
        postgres_user: Database username.
        postgres_password: Database password.
        redis_database: Redis database number.
        redis_host: Redis host address.
        redis_port: Redis port.
        redis_username: Redis username (optional).
        redis_password: Redis password.

    Example:
        >>> settings = get_settings()
        >>> print(settings.db_url)
        "postgresql+asyncpg://user:pass@host:5432/dbname"
    """

    # Logging
    log_level: str = ""
    log_format: str = ""

    # PostgreSQL
    postgres_db: str = ""
    postgres_host: str = ""
    postgres_port: int = 0
    postgres_user: str = ""
    postgres_password: str = ""

    @property
    def db_url(self) -> str:
        """
        Construct PostgreSQL connection URL.

        Returns:
            Full database connection string.
        """
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # Redis
    redis_database: int = 0
    redis_host: str = ""
    redis_port: int = 0
    redis_username: str = ""
    redis_password: str = ""

    @property
    def redis_url(self) -> str:
        """
        Construct Redis connection URL.

        Returns:
            Full Redis connection string.
        """
        return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_database}"

    # RabbitMQ
    rabbitmq_host: str = ""
    rabbitmq_port: int = 5672
    rabbitmq_default_user: str = ""
    rabbitmq_default_pass: str = ""
    rabbitmq_vhost: str = "/"

    @property
    def rabbitmq_url(self) -> str:
        """
        Construct RabbitMQ connection URL.

        Returns:
            Full RabbitMQ connection string (amqp protocol).
        """
        return (
            f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}{self.rabbitmq_vhost}"
        )

    model_config = SettingsConfigDict(extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings (cached singleton).

    Returns:
        Settings instance loaded from environment variables.
    """
    return Settings()
