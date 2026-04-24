import asyncio
import contextlib
import logging
import signal
import sys

from src.core.config import get_settings
from src.di import create_producer, create_tracker
from src.rabbitmq.rabbitmq_consumer import RabbitMQConsumer

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

    Starts two parallel processes:
    1. Site monitoring demon (check_all_sites)
    2. Subscription worker (listen for new sites via RabbitMQ)
    """
    from src.consumer_worker import subscribe_worker
    from src.producer_worker import check_demon

    logger = logging.getLogger(__name__)
    logger.info("Starting tracker service...")

    tracker = await create_tracker()
    producer = create_producer()
    consumer = RabbitMQConsumer()

    shutdown_event = asyncio.Event()

    def signal_handler():
        logger.info("Shutdown signal received...")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, signal_handler)

    try:
        await asyncio.gather(
            check_demon(tracker, producer),
            subscribe_worker(tracker, consumer),
            return_exceptions=True,
        )
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        raise
    finally:
        await producer.close()
        await consumer.close()
        logger.info("Services stopped")


if __name__ == "__main__":
    asyncio.run(main())
