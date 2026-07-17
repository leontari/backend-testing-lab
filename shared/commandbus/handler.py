"""Command handler contracts."""

from __future__ import annotations

from typing import Protocol, TypeVar

CommandT = TypeVar("CommandT")
ResultT = TypeVar("ResultT")


class CommandHandler(Protocol[CommandT, ResultT]):
    """
    Command handler protocol.

    Each command must have exactly
    one handler.

    Example:
        ChargePaymentCommand
                    |
                    v
        ChargePaymentHandler

    """

    async def handle(self, command: CommandT) -> ResultT:
        """
        Execute command.

        Parameters
        ----------
        command:
            Command object.

        Returns
        -------
        ResultT
            Command execution result.

        """
