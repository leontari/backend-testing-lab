"""
Base message abstraction.

Message is a transport envelope containing
payload and metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from shared.dto import DTO

if TYPE_CHECKING:
    from shared.messaging.metadata import MessageMetadata

PayloadT = TypeVar("PayloadT", bound=DTO)


@dataclass(frozen=True, slots=True)
class Message(Generic[PayloadT]):
    """
    Generic transport message.

    Structure:

        Message
            |
            + metadata
            |
            + payload DTO

    """

    metadata: MessageMetadata
    payload: PayloadT


__all__ = ("Message",)
