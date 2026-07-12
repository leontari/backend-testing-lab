from __future__ import annotations

import pytest


def test_current_empty(tracing):
    assert tracing.current() is None


@pytest.mark.asyncio
async def test_public_span_api(tracing):
    async with tracing.span() as span:
        assert tracing.current() == span
    assert tracing.current() is None


@pytest.mark.asyncio
async def test_extract_inject_cycle(tracing):
    async with tracing.span() as span:
        headers = {}
        tracing.inject(span, headers)

        extracted = tracing.extract(headers)

        assert extracted.trace_id == span.trace_id
