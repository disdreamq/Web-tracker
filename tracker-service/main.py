import asyncio
import logging
import sys

from src.core.config import get_settings

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=getattr(
        logging, settings.log_level.upper() if settings.log_level else "INFO"
    ),
    format=("%(asctime)s - %(name)s - %(levelname)s - " "%(message)s"),
    stream=sys.stdout,
)


async def main():
    """
    Application entry point.

    Starts the site tracking demon with optional RabbitMQ integration.
    """
    from src.worker import main as start_tracker

    logger = logging.getLogger(__name__)
    logger.info("Starting tracker service...")

    try:
        await start_tracker()
    except KeyboardInterrupt:
        logger.info("Shutdown requested...")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
