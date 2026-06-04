from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.dependencies import get_session_factory
from src.interfaces.rabbit_producer_interface import IRabbitMQProducer
from src.rabbitmq.rabbit_publisher import RabbitMQProducer
from src.user.repository import SQLAlchemyUserRepository
from src.user.service import UserService


async def get_producer() -> IRabbitMQProducer:
    return RabbitMQProducer()


async def get_user_service(
    session_factory: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_session_factory)
    ],
) -> UserService:
    return UserService(SQLAlchemyUserRepository(session_factory))
