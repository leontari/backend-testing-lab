"""
Runtime timer tests.
"""

import asyncio

import pytest

from metrics import Metrics



@pytest.mark.asyncio
async def test_async_timer_records_metric():


    metrics = Metrics()


    async with metrics.timer(
        "worker.duration_seconds"
    ):

        await asyncio.sleep(
            0.01
        )


    metric = (
        metrics.manager.get(
            "worker.duration_seconds"
        )
    )


    assert metric is not None



def test_sync_timer_records_metric():


    metrics = Metrics()


    with metrics.timer(
        "sync.duration_seconds"
    ):

        pass


    metric = (
        metrics.manager.get(
            "sync.duration_seconds"
        )
    )


    assert metric is not None
