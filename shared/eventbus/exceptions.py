"""EventBus exception definitions."""

from __future__ import annotations


class EventBusError(Exception):
    """Base EventBus exception."""


class HandlerRegistrationError(EventBusError):
    """Raised when handler registration fails."""


class HandlerNotFoundError(EventBusError):
    """Raised when no handler exists."""


class EventDispatchError(EventBusError):
    """Raised when event dispatch fails."""
