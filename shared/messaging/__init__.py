"""
Shared messaging framework.

Provides transport-independent message abstractions.
"""
from __future__ import annotations

from shared.messaging.exceptions import (
    EnvelopeError,
    HeaderError,
    MessageDeserializationError,
    MessageSerializationError,
    MessageValidationError,
    MessagingError,
    MetadataError,
)
from shared.messaging.headers import HeaderKeys, MessageHeaders
from shared.messaging.identity import MessageIdentity
from shared.messaging.message import Message, MessageKind
from shared.messaging.metadata import (
    MessageMetadata,
    MetadataKeys,
    RuntimeStatus,
)

__all__ = (
    "EnvelopeError",
    "HeaderError",
    "HeaderKeys",
    "Message",
    "MessageDeserializationError",
    "MessageHeaders",
    "MessageIdentity",
    "MessageKind",
    "MessageMetadata",
    "MessageSerializationError",
    "MessageSerializer",
    "MessageValidationError",
    "MessagingError",
    "MetadataError",
    "MetadataKeys",
    "Payload",
    "RuntimeStatus",
)

from shared.messaging.payload import Payload
from shared.messaging.serializer import MessageSerializer
