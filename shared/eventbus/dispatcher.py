"""Event execution dispatcher."""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(slots=True)
class EventDispatcher:
    """Executes handlers."""

    async def dispatch(self, handler: object, event: Callable) -> None:
        method = getattr(handler, "handle")
        result = method(event)

        if inspect.isawaitable(result):
            await result
