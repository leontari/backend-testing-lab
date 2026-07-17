"""Event handler registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import TYPE_CHECKING

from shared.eventbus.exceptions import HandlerRegistrationError

if TYPE_CHECKING:
    from shared.messaging import Event


@dataclass(slots=True, frozen=True)
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
    _lock: RLock = field(init=False, default_factory=RLock)

    def register(self, event_type: type[Event], handler: object) -> None:
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

    def resolve(self, event_type: type[Event]) -> tuple[object, ...]:
        """
        Resolve handlers.

        Returns
        -------
        tuple[object,...]
            Immutable handler collection.

        """
        with self._lock:
            return tuple(self._handlers.get(event_type, ()))
