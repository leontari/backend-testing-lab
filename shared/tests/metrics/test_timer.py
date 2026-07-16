"""Tests for MetricTimer."""
from __future__ import annotations

from unittest.mock import Mock

import pytest

from shared.metrics.timer import MetricTimer





def test_sync_timer(histogram):
    timer = MetricTimer(histogram)

    with timer:
        pass

    context = histogram.time.return_value

    assert context.entered
    assert context.exited


@pytest.mark.asyncio
async def test_async_timer(histogram):
    timer = MetricTimer(histogram)

    async with timer:
        pass

    context = histogram.time.return_value

    assert context.entered
    assert context.exited
