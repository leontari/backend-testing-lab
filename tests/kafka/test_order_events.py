import pytest
import asyncio
from tests.helpers.kafka_consumer import TestKafkaConsumer
from tests.helpers.kafka_wait import wait_for_event


@pytest.mark.asyncio
async def test_order_event_emission():

    consumer = TestKafkaConsumer("order.created")
    await consumer.start()

    # simulate delay for system propagation
    await asyncio.sleep(2)

    event = wait_for_event(
        consumer,
        lambda e: "order_id" in e,
        timeout=20
    )

    assert event["order_id"] is not None

    await consumer.stop()
