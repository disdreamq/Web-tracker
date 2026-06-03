from src.interfaces.rabbit_producer_interface import IRabbitMQProducer
from src.rabbitmq.rabbit_publisher import RabbitMQProducer


async def get_producer() -> IRabbitMQProducer:
    return RabbitMQProducer()
