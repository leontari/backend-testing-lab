from fastapi import FastAPI
from fastapi.testclient import TestClient

from shared.tracing.fastapi import TraceMiddleware
from shared.tracing.manager import TraceManager


def test_fastapi_full_trace_flow():
    app = FastAPI()
    manager = TraceManager()

    app.add_middleware(TraceMiddleware, trace_manager=manager)

    @app.get("/ping")
    async def ping():
        trace = manager.get_current_trace()
        return {
            "trace_id": trace.trace_id,
            "span_id": trace.span_id,
        }

    client = TestClient(app)

    response = client.get(
        "/ping",
        headers={
            "traceparent": "00-" + "a" * 32 + "-" + "b" * 16 + "-01"
        },
    )

    assert response.status_code == 200
    assert "trace_id" in response.json()
    assert "span_id" in response.json()

    # response headers propagation
    assert "traceparent" in response.headers
