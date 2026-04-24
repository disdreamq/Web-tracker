import asyncio
import contextlib
import signal
from asyncio import Task
from logging import getLogger

from src.core.config import get_settings
from src.rabbitmq.rabbitmq_publisher import RabbitMQProducer
from src.tracker.tracker import Tracker

logger = getLogger(__name__)


async def check_demon(
    tracker: Tracker,
    producer: RabbitMQProducer,
    check_interval: int = 5,
) -> None:
    """
    Demon that periodically checks all tracked sites for changes.

    Runs an infinite loop that checks all sites for content changes
    and sends notifications via RabbitMQ when changes are detected.
    Supports graceful shutdown on SIGTERM/SIGINT.

    Args:
        tracker: Tracker instance for checking sites.
        producer: RabbitMQ producer for sending notifications.
        check_interval: Interval between checks in seconds.

    Example:
        >>> tracker = await create_tracker()
        >>> producer = create_producer()
        >>> await check_demon(tracker, producer, check_interval=10)
    """
    settings = get_settings()
    check_interval = getattr(settings, "check_interval", check_interval)

    shutdown_event = asyncio.Event()
    current_check: Task | None = None

    def signal_handler():
        logger.info("Shutdown signal received, stopping gracefully...")
        shutdown_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, signal_handler)

    logger.info("Check demon started")

    try:
        while not shutdown_event.is_set():
            try:
                check_task = asyncio.create_task(tracker.check_all_sites())
                current_check = check_task

                if updated_sites := await check_task:
                    for url in updated_sites:
                        try:
                            await producer.publish(
                                exchange=settings.rabbitmq_exchange_name,
                                routing_key=settings.rabbitmq_routing_key_updated,
                                message={"url": url, "status": "updated"},
                            )
                            logger.info("Sent update notification for: %s", url)
                        except Exception as e:
                            logger.error(
                                "Failed to publish notification for %s: %s", url, e
                            )

                try:
                    await asyncio.wait_for(
                        shutdown_event.wait(), timeout=check_interval
                    )
                    break
                except TimeoutError:
                    continue

            except Exception as e:
                logger.error("Error in check demon: %s", e)
                await asyncio.sleep(check_interval)

    finally:
        if current_check and not current_check.done():
            current_check.cancel()
            with contextlib.suppress(TimeoutError, asyncio.CancelledError):
                await asyncio.wait_for(current_check, timeout=1.0)

        logger.info("Check demon stopped")
