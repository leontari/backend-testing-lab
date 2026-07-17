"""
Message envelope.

Transport representation of messages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from shared.messaging.metadata import (
    MessageMetadata,
)


@dataclass(
    frozen=True,
    slots=True,
)
class MessageEnvelope:
    """
    Serialized transport message.

    Used by adapters:

    - Kafka
    - HTTP
    - gRPC
    """

    message_type: str

    version: int

    metadata: MessageMetadata

    payload: dict[str, Any]


__all__ = (
    "MessageEnvelope",
)
