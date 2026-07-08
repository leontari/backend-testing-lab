"""
Runtime TraceContext storage.

This module encapsulates ContextVar and provides an async-safe
storage for TraceContext instances.

Only TraceContextStore interacts directly with ContextVar.
"""

from __future__ import annotations

from contextvars import ContextVar, Token
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import TraceContext


class TraceContextStore:
    """
    Async-safe runtime TraceContext storage.

    The store provides isolation between asyncio Tasks
    and HTTP requests.

    Notes
    -----
    This class is the only component that accesses ContextVar
    directly.

    """

    def __init__(self) -> None:
        """Initialize runtime storage."""
        self._context: ContextVar[TraceContext | None] = ContextVar(
            "trace_context",
            default=None,
        )

    def get_current_trace(self) -> TraceContext | None:
        """
        Get current TraceContext.

        Returns
        -------
            TraceContext | None - Current trace or None.

        """
        return self._context.get()

    def set_current_trace(
        self,
        trace: TraceContext,
    ) -> Token[TraceContext | None]:
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

    def reset_current_trace(
        self,
        token: Token[TraceContext | None],
    ) -> None:
        """
        Restore previous TraceContext.

        Parameters
        ----------
        token:
            Token returned by set_current_trace().

        """
        self._context.reset(token)

    def clear_for_testing(self) -> None:
        """
        Remove active TraceContext.

        Notes
        -----
        Intended for unit tests only.

        """
        self._context.set(None)
