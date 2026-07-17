"""
Shared messaging framework.

Provides transport-independent
message abstractions.
"""
from __future__ import annotations

from shared.messaging.command import Command
from shared.messaging.envelop import MessageEnvelope
from shared.messaging.event import Event
from shared.messaging.message import Message
from shared.messaging.metadata import MessageMetadata, create_metadata

__all__ = (
    "Command",
    "Event",
    "Message",
    "MessageEnvelope",
    "MessageMetadata",
    "create_metadata",
)
