import asyncio
import json
import asyncpg
from aiokafka import AIOKafkaConsumer


async def main():

    db = await asyncpg.create_pool(
        user="app",
        password="app",
        database="notification_db",
        host="postgres-notification",
    )

    consumer = AIOKafkaConsumer(
        "payment.completed",
        bootstrap_servers="kafka:9092",
        group_id="notification-group",
    )

    await consumer.start()

    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode())

            async with db.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO notifications(id, payload)
                    VALUES($1, $2)
                    """,
                    event["payment_id"],
                    json.dumps(event),
                )

    finally:
        await consumer.stop()
