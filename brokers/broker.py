from faststream.rabbit import RabbitBroker, RabbitMessage
from config import RABBIT_HOST
import logging
import asyncio
import json

from managers.Logger import AsyncLogger

print(f"amqp://guest:guest@{RABBIT_HOST}:5672/")
logger = AsyncLogger()


class SafeRabbitBroker(RabbitBroker):
    async def safe_start(self, attempts_count=3, interval=3):
        for _ in range(attempts_count):
            try:
                await self.start()
                return
            except Exception as ex:
                await asyncio.sleep(interval)

        await self.start()

    async def safe_publish(self, *args, **kwargs):
        try:
            await super().publish(*args, **kwargs)
            await logger.log("Rabbit publish success")
        except Exception as ex:
            await logger.error(f"Error while publishing to rabbit\n{ex}")


broker = SafeRabbitBroker(host=RABBIT_HOST)


def decoder(msg):
    msg.body = json.loads(msg.body.decode())
