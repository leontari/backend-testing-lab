"""CommandBus exceptions."""

from __future__ import annotations


class CommandBusError(Exception):
    """Base CommandBus exception."""


class HandlerRegistrationError(CommandBusError):
    """Raised when command handler registration fails."""


class HandlerNotFoundError(CommandBusError):
    """Raised when command has no handler."""


class CommandExecutionError(CommandBusError):
    """Raised when command execution fails."""
