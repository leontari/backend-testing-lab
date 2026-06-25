import asyncio

import pytest

from tests.helpers.kafka_consumer import TestKafkaConsumer


@pytest.mark.asyncio
async def test_no_duplicate_events():

    consumer = TestKafkaConsumer("order.created")
    await consumer.start()

    await asyncio.sleep(5)

    ids = [e["order_id"] for e in consumer.messages]

    assert len(ids) == len(set(ids))

    await consumer.stop()
