"""Locust base scenario."""
from locust import HttpUser, task, between
import uuid


class OrderUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.api_key = "secret"

    @task
    def create_order(self):
        payload = {
            "payload": {
                "product": "book",
                "price": 100
            }
        }

        self.client.post(
            "/orders",
            json=payload,
            headers={"x-api-key": self.api_key},
        )
