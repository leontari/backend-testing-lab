"""
Tracing runtime manager.

Responsible for trace lifecycle management.

Responsibilities:

- access current TraceContext
- create child/root spans
- activate execution context
- restore previous context

"""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from .factory import TraceFactory
    from .models import TraceContext
    from .store import TraceContextStore


@dataclass(slots=True, frozen=True)
class TraceManager:
    """Runtime trace lifecycle manager."""

    factory: TraceFactory = field(default_factory=TraceFactory)
    store: TraceContextStore = field(default_factory=TraceContextStore)

    def current(self) -> TraceContext | None:
        """
        Return active trace context.

        Returns
        -------
        TraceContext | None
            Current execution trace.

        """
        return self.store.current()

    def create(
        self,
        source: TraceContext | None = None,
    ) -> TraceContext:
        """
        Create new trace context.

        Parameters
        ----------
        source:
            Existing context.

        Behavior
        --------
        source=None:
            create root trace.

        source=TraceContext:
            create child span.
        """

        return self.factory.create(source)

    def activate(self, context: TraceContext):
        """
        Activate trace context.

        Returns
        -------
        Token
            ContextVar reset token.

        """
        return self._store.set(context)

    def deactivate(self, token) -> None:
        """Restore previous context."""
        self._store.reset(token)

    @asynccontextmanager
    async def span(
        self,
        source: TraceContext | None = None,
    ) -> AsyncIterator[TraceContext]:
        """
        Create and activate execution span.

        Example
        -------
        async with manager.span():
            await operation()

        Lifecycle:
        current context
        |
        v
        create child
        |
        v
        set ContextVar
        |
        v
        execute code
        |
        v
        reset ContextVar

        """
        if source is None:
            source = self.current()

        context = self.create(source)
        token = self.activate(context)

        try:
            yield context
        finally:
            self.deactivate(token)


__all__ = ("TraceManager",)
