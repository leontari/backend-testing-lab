"""Event handler contracts."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from shared.messaging import Event


class EventHandler(Protocol):
    """
    Event handler protocol.

    Handlers may be:
    - async;
    - sync.

    """

    async def handle(self, event: Event) -> None:
        """
        Handle event.

        Parameters
        ----------
        event:
            Incoming event.

        """
