"""
Command message definitions.

Commands represent requested actions.
"""

from __future__ import annotations

from dataclasses import dataclass

from shared.dto import DTO
from shared.messaging.message import Message


@dataclass(frozen=True, slots=True)
class Command(Message[DTO]):
    """
    Base command message.

    Example:
        CreatePaymentCommand

    Meaning:
        Please perform this action.

    """


__all__ = ("Command",)
