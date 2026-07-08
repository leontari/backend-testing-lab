"""
Structured logging with distributed trace correlation.

This module binds TraceContext to Python logging system,
allowing automatic enrichment of log records with:

- trace_id
- span_id
- parent_span_id
- sampling flags

It is fully ContextVar-safe and async-friendly.
"""

from __future__ import annotations

import logging
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.tracing.manager import TraceManager

_log_context: ContextVar[dict[str, str] | None] = ContextVar(
    "trace_log_context",
    default=None,
)


class TraceLoggingFilter(logging.Filter):
    """Logging filter that injects trace context into log records."""

    def __init__(self, trace_manager: TraceManager) -> None:
        """
        Initialize trace logging filter.

        Parameters
        ----------
        trace_manager:
            Runtime trace manager.

        """
        super().__init__()
        self._trace_manager = trace_manager

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Enrich log record with trace context.

        Returns
        -------
        bool
            Always True (log record is not filtered).

        """
        try:
            trace = self._trace_manager.get_current_trace()

            record.trace_id = trace.trace_id
            record.span_id = trace.span_id
            record.parent_span_id = trace.parent_span_id

        except Exception:
            # No active trace → safe fallback
            record.trace_id = None
            record.span_id = None
            record.parent_span_id = None

        return True


def get_log_context() -> dict[str, str] | None:
    """
    Return current logging context.

    Returns
    -------
    dict[str, str]
        Trace-aware structured log context.

    """
    return _log_context.get()
