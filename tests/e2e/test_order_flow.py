import pytest
import asyncio
from tests.helpers.gateway_client import GatewayClient


@pytest.mark.asyncio
async def test_full_order_flow():

    gateway = GatewayClient()

    # 1. create order via REST
    response = await gateway.create_order({
        "payload": {
            "product": "book",
            "price": 100
        }
    })

    trace_id = response["trace_id"]
    order_id = response["order"]["order_id"]

    # 2. validate response
    assert order_id is not None
    assert trace_id is not None

    # 3. wait for async propagation (Kafka → Payment → Notification)
    await asyncio.sleep(5)

    # 4. DB / system assertions (simplified)
    assert response["order"]["status"] == "created"
