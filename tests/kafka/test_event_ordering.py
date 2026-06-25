import asyncio

import pytest

from tests.helpers.kafka_consumer import TestKafkaConsumer


@pytest.mark.asyncio
async def test_event_order():

    consumer = TestKafkaConsumer("order.created")
    await consumer.start()

    await asyncio.sleep(5)

    timestamps = [
        e.get("timestamp", 0)
        for e in consumer.messages
    ]

    assert timestamps == sorted(timestamps)

    await consumer.stop()
