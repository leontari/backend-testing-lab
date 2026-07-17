"""Event error policies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(slots=True)
class ErrorPolicy:
    """
    Defines event failure behaviour.

    dead_letter:
        Called after retry exhaustion.
    """

    dead_letter: Callable | None = None


__all__ = ("ErrorPolicy",)
