import asyncio

from shared.tracing.factory import TraceFactory
from shared.tracing.manager import TraceManager


def test_context_isolation(trace_manager: TraceManager) -> None:
    trace1 = TraceFactory.create_root_trace()
    trace2 = TraceFactory.create_root_trace()

    token1 = manager.install_trace(trace1)
    active1 = manager.get_current_trace()

    manager.restore_trace(token1)

    token2 = manager.install_trace(trace2)
    active2 = manager.get_current_trace()

    manager.restore_trace(token2)

    assert active1.trace_id == trace1.trace_id
    assert active2.trace_id == trace2.trace_id
    assert active1.trace_id != active2.trace_id


def test_async_context_isolation():
    manager = TraceManager()

    async def task(trace):
        token = manager.install_trace(trace)
        current = manager.get_current_trace()
        manager.restore_trace(token)
        return current.trace_id

    async def run():
        t1 = TraceFactory.create_root_trace()
        t2 = TraceFactory.create_root_trace()

        r1, r2 = await asyncio.gather(task(t1), task(t2))

        assert r1 != r2

    asyncio.run(run())
