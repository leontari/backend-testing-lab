"""
Application CommandBus.

CommandBus executes application commands.

Characteristics:
- one command;
- one handler;
- sequential execution;
- returns result.

CommandBus does not:
- publish events;
- manage workflows;
- know transports.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from shared.commandbus.dispatcher import CommandDispatcher
from shared.commandbus.exceptions import (
    CommandExecutionError,
    HandlerNotFoundError,
)
from shared.commandbus.registry import CommandRegistry


@dataclass(slots=True)
class CommandBus:
    """
    Application command dispatcher.

    Example:
        result = await bus.execute(ChargePaymentCommand(...))

    """

    _registry: CommandRegistry = field(default_factory=CommandRegistry)
    _dispatcher: CommandDispatcher = field(default_factory=CommandDispatcher)

    def register(self, command_type: type, handler: object) -> None:
        """Register command handler."""
        self._registry.register(command_type, handler)

    async def execute(self, command):
        """
        Execute command.

        Parameters
        ----------
        command:
            Command instance.

        Returns
        -------
        object
            Handler result.

        Raises
        ------
        HandlerNotFoundError
            No handler registered.

        CommandExecutionError
            Handler failed.

        """
        handler = self._registry.resolve(type(command))

        if handler is None:
            msg = f"No handler for {type(command).__name__}"
            raise HandlerNotFoundError(msg)

        try:
            return await self._dispatcher.dispatch(handler, command)

        except Exception as exc:
            msg = f"Failed executing {type(command).__name__}"
            raise CommandExecutionError(msg) from exc
