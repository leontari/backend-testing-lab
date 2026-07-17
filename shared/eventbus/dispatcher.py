"""Event execution dispatcher."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.messaging import Event


class EventDispatcher:
    """
    Executes event handlers.

    Supports:
    - sync handlers;
    - async handlers.
    """

    @classmethod
    async def dispatch(cls, handler: object, event: Event) -> None:
        """Execute handler."""
        method = getattr(handler, "handle")
        result = method(event)

        if inspect.isawaitable(result):
            await result
