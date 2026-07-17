"""
Event message definitions.

Events represent facts that already happened.
"""

from __future__ import annotations

from dataclasses import dataclass

from shared.dto import DTO
from shared.messaging.message import Message


@dataclass(frozen=True, slots=True)
class Event(Message[DTO]):
    """
    Base event message.

    Example:
        PaymentCompletedEvent

    Meaning:

        Something happened.

    Events should be immutable.

    """


__all__ = ("Event",)
