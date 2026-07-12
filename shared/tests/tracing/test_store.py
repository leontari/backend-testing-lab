from __future__ import annotations

import pytest

from shared.tracing.models import TraceContext
from shared.tracing.store import TraceContextStore


@pytest.mark.asyncio
async def test_store_set_and_get():
    store = TraceContextStore()
    context = TraceContext(
        trace_id="trace-1",
        span_id="span-1",
    )

    token = store.set(context)

    try:
        assert store.current() == context
    finally:
        store.reset(token)


@pytest.mark.asyncio
async def test_store_returns_none_without_context():
    store = TraceContextStore()

    assert store.get() is None


@pytest.mark.asyncio
async def test_context_isolation_between_tasks():
    import asyncio

    store = TraceContextStore()

    async def worker(value):
        ctx = TraceContext(trace_id=value, span_id="span")
        token = store.set(ctx)

        try:
            await asyncio.sleep(0)

            return store.get()

        finally:
            store.reset(token)

    result = await asyncio.gather(worker("A"), worker("B"))

    assert result[0].trace_id == "A"
    assert result[1].trace_id == "B"
