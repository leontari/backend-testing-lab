"""Command handler registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock

from shared.commandbus.exceptions import HandlerRegistrationError


@dataclass(slots=True)
class CommandRegistry:
    """
    Stores command-handler mapping.

    Unlike EventBus:
        one command -> one handler

    """

    _handlers: dict[type, object] = field(default_factory=dict)
    _lock: RLock = field(init=False, default_factory=RLock)

    def register(self, command_type: type, handler: object) -> None:
        """
        Register command handler.

        Raises
        ------
        HandlerRegistrationError
            If handler already exists.

        """
        with self._lock:
            if command_type in self._handlers:
                msg = f"Handler already exists for {command_type.__name__}"
                raise HandlerRegistrationError(msg)

            self._handlers[command_type] = handler

    def resolve(self, command_type: type) -> object | None:
        """
        Resolve command handler.

        Returns
        -------
        object | None
            Handler instance.

        """
        with self._lock:
            return self._handlers.get(command_type)
