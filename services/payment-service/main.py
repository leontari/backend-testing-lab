import grpc
from concurrent import futures
import asyncpg
import json
import uuid
from aiokafka import AIOKafkaProducer
import asyncio

import payment_pb2
import payment_pb2_grpc


class PaymentService(payment_pb2_grpc.PaymentServiceServicer):

    def __init__(self):
        self.db = None
        self.kafka = None

    async def init(self):
        self.db = await asyncpg.create_pool(
            user="app",
            password="app",
            database="payment_db",
            host="postgres-payment",
        )

        self.kafka = AIOKafkaProducer(
            bootstrap_servers="kafka:9092"
        )
        await self.kafka.start()

    async def ProcessPayment(self, request, context):

        payment_id = str(uuid.uuid4())

        async with self.db.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO payments(id, order_id)
                VALUES($1, $2)
                """,
                payment_id,
                request.order_id,
            )

        event = {
            "payment_id": payment_id,
            "order_id": request.order_id,
            "trace_id": request.trace_id,
        }

        await self.kafka.send_and_wait(
            "payment.completed",
            json.dumps(event).encode(),
        )

        return payment_pb2.PaymentResponse(
            payment_id=payment_id,
            status="completed",
        )


async def serve():
    server = grpc.aio.server()
    service = PaymentService()

    await service.init()

    payment_pb2_grpc.add_PaymentServiceServicer_to_server(
        service, server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()
