import json
import uuid

import asyncpg
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DB = None
KAFKA = None


class OrderIn(BaseModel):
    payload: dict
    trace_id: str


@app.on_event("startup")
async def startup():
    global DB, KAFKA

    DB = await asyncpg.create_pool(
        user="app",
        password="app",
        database="order_db",
        host="postgres-order",
    )

    KAFKA = AIOKafkaProducer(
        bootstrap_servers="kafka:9092"
    )

    await KAFKA.start()


@app.on_event("shutdown")
async def shutdown():
    await KAFKA.stop()
    await DB.close()


@app.post("/orders")
async def create_order(order: OrderIn):
    order_id = str(uuid.uuid4())

    async with DB.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO orders(id, payload)
            VALUES($1, $2)
            """,
            order_id,
            json.dumps(order.payload),
        )

    event = {
        "order_id": order_id,
        "trace_id": order.trace_id,
    }

    await KAFKA.send_and_wait(
        "order.created",
        json.dumps(event).encode(),
    )

    return {
        "order_id": order_id,
        "status": "created",
    }
