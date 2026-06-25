from fastapi import FastAPI, Header, HTTPException
import httpx
import uuid

app = FastAPI()

ORDER_SERVICE_URL = "http://order-service:8000"

API_KEY = "secret"


@app.post("/orders")
async def create_order(
    payload: dict,
    x_api_key: str = Header(None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    trace_id = str(uuid.uuid4())

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ORDER_SERVICE_URL}/orders",
            json={
                "payload": payload,
                "trace_id": trace_id,
            },
        )

    return {
        "trace_id": trace_id,
        "order": response.json(),
    }
