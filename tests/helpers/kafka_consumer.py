import asyncio
from aiokafka import AIOKafkaConsumer
import json


class TestKafkaConsumer:

    def __init__(self, topic, group_id="test-group"):
        self.topic = topic
        self.group_id = group_id
        self.messages = []

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers="localhost:9092",
            group_id=self.group_id,
            auto_offset_reset="earliest",
        )

        await self.consumer.start()

        asyncio.create_task(self._consume())

    async def _consume(self):
        async for msg in self.consumer:
            self.messages.append(
                json.loads(msg.value.decode())
            )

    async def stop(self):
        await self.consumer.stop()
