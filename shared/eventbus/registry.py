"""Event handler registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import TYPE_CHECKING

from shared.eventbus.exceptions import HandlerRegistrationError

if TYPE_CHECKING:
    from shared.messaging import Event


@dataclass(slots=True)
class EventRegistry:
    """
    Thread-safe event handler registry.

    Stores event-handler relations.

    Example:
        PaymentCreatedEvent
              |
              +-- EmailHandler
              +-- MetricsHandler

    """

    _handlers: dict[type[Event], list[object]] = field(default_factory=dict)
    _lock: RLock = field(default_factory=RLock, init=False)

    def register(
        self,
        event_type: type[Event],
        handler: object,
    ) -> None:
        """
        Register event handler.

        Raises
        ------
        HandlerRegistrationError
            Duplicate handler.

        """
        with self._lock:
            handlers = self._handlers.setdefault(event_type, [])

            if handler in handlers:
                msg = "Handler already registered"
                raise HandlerRegistrationError(msg)

            handlers.append(handler)

    def get(self, event_type: type[Event]) -> tuple[object, ...]:
        """
        Get handlers.

        Returns
        -------
        tuple[object,...]
            Registered handlers.

        """
        with self._lock:
            return tuple(self._handlers.get(event_type, ()))
