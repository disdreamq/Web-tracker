from .rabbit_consumer import RabbitMQConsumer
from .rabbit_publisher import RabbitMQProducer

consumer = RabbitMQConsumer()
producer = RabbitMQProducer()

async def get_consumer() -> RabbitMQConsumer:
    return consumer

async def get_producer() -> RabbitMQProducer:
    return producer
