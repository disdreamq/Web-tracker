import asyncio

from src.worker import main as start


async def main():
    await start()


if __name__ == "__main__":
    asyncio.run(main())
