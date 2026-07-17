from __future__ import annotations

from shared.logger.context import (
    LogContext,
    current_context,
    reset_context,
    set_context,
)


def test_default_context() -> None:
    """Empty context should exist by default."""
    context = current_context()
    assert context.fields == {}


def test_set_and_restore_context() -> None:
    """ContextVar should restore previous state."""
    token = set_context(LogContext({"trace_id": "abc"}))
    try:
        context = current_context()
        assert context.fields["trace_id"] == "abc"
    finally:
        reset_context(token)
    assert current_context().fields == {}


def test_context_is_immutable() -> None:
    """LogContext should be frozen."""
    context = LogContext({"key": "value"})
    try:
        context.fields = {}
    except AttributeError:
        pass
    else:
        msg = "LogContext must be frozen"
        raise AssertionError(msg)
