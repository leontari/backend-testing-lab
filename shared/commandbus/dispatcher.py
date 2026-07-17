"""Command dispatcher."""

from __future__ import annotations

import inspect


class CommandDispatcher:
    """
    Executes command handlers.

    Supports:
    - sync handlers;
    - async handlers.
    """

    async def dispatch(self, handler: object, command):
        """Execute handler."""
        method = getattr(handler, "handle")
        result = method(command)

        if inspect.isawaitable(result):
            return await result

        return result
