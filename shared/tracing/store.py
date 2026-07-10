"""
Async runtime trace context storage.

This module encapsulates ContextVar and provides an async-safe
storage for TraceContext instances.

"""

from __future__ import annotations

from contextvars import ContextVar, Token
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import TraceContext


class TraceContextStore:
    """
    Async-safe runtime trace context storage.

    ContextVar provides isolation between:
    - asyncio tasks;
    - concurrent requests;
    - background coroutines;

    """

    def __init__(self) -> None:
        """Initialize runtime storage."""
        self._context: ContextVar[TraceContext | None] = ContextVar(
            "trace_context",
            default=None,
        )

    def current(self) -> TraceContext | None:
        """
        Get current TraceContext.

        Returns
        -------
            TraceContext | None - Current trace or None.

        """
        return self._context.get()

    def set(self, trace: TraceContext) -> Token[TraceContext | None]:
        """
        Install TraceContext.

        Parameters
        ----------
        trace:
            Runtime TraceContext.

        Returns
        -------
        Token
            ContextVar rollback token.

        """
        return self._context.set(trace)

    def reset(self, token: Token[TraceContext | None]) -> None:
        """
        Restore previous TraceContext.

        Parameters
        ----------
        token:
            Token returned by set().

        """
        self._context.reset(token)

    def clear(self) -> None:
        """
        Remove active TraceContext.

        Notes
        -----
        Intended for unit tests only.

        """
        self._context.set(None)
