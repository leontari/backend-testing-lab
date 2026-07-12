import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from shared.tracing.fastapi import TraceMiddleware
from shared.tracing.tracing import Tracing


@pytest.mark.asyncio
async def test_fastapi_trace_middleware():
    tracing = Tracing()
    app = FastAPI()

    app.add_middleware(TraceMiddleware, tracing=tracing)


    @app.get("/")
    async def index():
        ctx = tracing.current()
        return {"trace_id": ctx.trace_id}


    async with AsyncClient(base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json()["trace_id"]
