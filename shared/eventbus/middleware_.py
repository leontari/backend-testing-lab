"""EventBus middleware support."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Callable

    from shared.messaging import Event


class EventMiddleware(Protocol):
    """
    Event processing middleware.

    Similar to:
    - HTTP middleware;
    - Kafka interceptor.

    """

    async def __call__(self, event: Event, next_handler: Callable) -> None:
        """Process event middleware."""
