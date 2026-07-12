import pytest

from shared.tracing.factory import TraceFactory
from shared.tracing.manager import TraceManager
from shared.tracing.store import TraceContextStore


@pytest.fixture
def manager():
    return TraceManager(
        factory=TraceFactory(),
        store=TraceContextStore(),
    )

def test_current_without_span(manager):
    assert manager.current() is None


@pytest.mark.asyncio
async def test_span_sets_context(manager):
    async with manager.span() as span:
        current = manager.current()
        assert current == span
    assert manager.current() is None


@pytest.mark.asyncio
async def test_nested_span_restore(manager):
    async with manager.span() as parent:
        async with manager.span() as child:
            assert child.parent_span_id == parent.span_id
        assert manager.current() == parent
    assert manager.current() is None


@pytest.mark.asyncio
async def test_context_restored_after_exception(manager):
    with pytest.raises(ValueError):
        async with manager.span():
            raise ValueError()

    assert manager.current() is None
