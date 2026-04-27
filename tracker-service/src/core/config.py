import logging
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

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
    - RabbitMQ

    Attributes:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR).
        postgres_db: Database name.
        postgres_host: Database host address.
        postgres_port: Database port.
        postgres_user: Database username.
        postgres_password: Database password.
        redis_database: Redis database number.
        redis_host: Redis host address.
        redis_port: Redis port.
        redis_password: Redis password.
        rabbitmq_host: RabbitMQ host address.
        rabbitmq_port: RabbitMQ port.
        rabbitmq_default_user: RabbitMQ username.
        rabbitmq_default_pass: RabbitMQ password.
        rabbitmq_vhost: RabbitMQ virtual host.

    Example:
        >>> settings = get_settings()
        >>> print(settings.db_url)
        "postgresql+asyncpg://user:pass@host:5432/dbname"
    """

    # Logging
    log_level: str = "INFO"

    # PostgreSQL
    postgres_db: str = ""
    postgres_host: str = ""
    postgres_port: int = 5432
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
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    # RabbitMQ
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_default_user: str = "guest"
    rabbitmq_default_pass: str = "guest"
    rabbitmq_vhost: str = "/"

    @property
    def rabbitmq_url(self) -> str:
        """
        Construct RabbitMQ connection URL.

        Returns:
            Full RabbitMQ connection string (amqp protocol).
        """
        return (
            f"amqp://{self.rabbitmq_default_user}:"
            f"{quote(self.rabbitmq_default_pass, safe='')}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}{self.rabbitmq_vhost}"
        )

    # RabbitMQ queues and exchanges
    rabbitmq_exchange_name: str = "sites"
    rabbitmq_queue_new: str = "new_sites"
    rabbitmq_queue_updated: str = "updated_sites"
    rabbitmq_routing_key_new: str = "new"
    rabbitmq_routing_key_updated: str = "updated"

    model_config = SettingsConfigDict(extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings (cached singleton).

    Returns:
        Settings instance loaded from environment variables.
    """
    return Settings()
