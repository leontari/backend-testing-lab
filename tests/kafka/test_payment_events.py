import pytest
import asyncio
from tests.helpers.kafka_consumer import TestKafkaConsumer
from tests.helpers.kafka_assertions import assert_event_chain


@pytest.mark.asyncio
async def test_payment_event_chain():

    order_consumer = TestKafkaConsumer("order.created")
    payment_consumer = TestKafkaConsumer("payment.completed")

    await order_consumer.start()
    await payment_consumer.start()

    await asyncio.sleep(5)

    assert len(order_consumer.messages) > 0
    assert len(payment_consumer.messages) > 0

    order_event = order_consumer.messages[0]
    payment_event = payment_consumer.messages[0]

    assert_event_chain(order_event, payment_event)

    await order_consumer.stop()
    await payment_consumer.stop()
