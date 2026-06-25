import httpx


class GatewayClient:

    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.headers = {"x-api-key": "secret"}

    async def create_order(self, payload):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.base_url}/orders",
                json=payload,
                headers=self.headers,
            )
        return r.json()
