"""
Metrics integration tests.

Tests complete runtime flow:

Metrics
    |
MetricManager
    |
Prometheus backend
    |
FastAPI /metrics endpoint
"""

from __future__ import annotations


import pytest

from fastapi import FastAPI
from httpx import AsyncClient
from httpx import ASGITransport

from prometheus_client import (
    make_asgi_app,
)

from metrics import Metrics



@pytest.fixture
def metrics():

    return Metrics()



@pytest.fixture
def app(
    metrics,
):

    app = FastAPI()


    app.state.metrics = metrics


    app.mount(
        "/metrics",
        make_asgi_app(),
    )


    @app.get(
        "/orders"
    )
    async def create_order():

        metrics.increment(
            "orders_created_total",
        )

        return {
            "status": "ok"
        }


    return app



@pytest.mark.asyncio
async def test_metrics_endpoint_available(
    app,
):

    transport = ASGITransport(
        app=app
    )


    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:


        response = await client.get(
            "/metrics"
        )


    assert response.status_code == 200



@pytest.mark.asyncio
async def test_counter_exported(
    app,
):

    transport = ASGITransport(
        app=app
    )


    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:


        await client.get(
            "/orders"
        )


        response = await client.get(
            "/metrics"
        )


    assert (
        "orders_created_total"
        in response.text
    )



@pytest.mark.asyncio
async def test_histogram_exported(
    app,
    metrics,
):

    metrics.observe(
        "request_duration_seconds",
        0.15,
    )


    transport = ASGITransport(
        app=app
    )


    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:


        response = await client.get(
            "/metrics"
        )


    assert (
        "request_duration_seconds"
        in response.text
    )
