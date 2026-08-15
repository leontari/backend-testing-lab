"""
Messaging exceptions.

This module defines the exception hierarchy used by the messaging
subsystem.

The messaging layer is transport-agnostic and shared by:

- CommandBus;
- EventBus;
- Workflow Engine;
- HTTP adapters;
- gRPC adapters;
- Kafka adapters.

Application code should normally catch ``MessagingError`` or one of
its subclasses.
"""

from __future__ import annotations


class MessagingError(Exception):
    """
    Base messaging exception.

    Every exception raised by the messaging subsystem inherits from
    this class.
    """


class MessageValidationError(MessagingError):
    """
    Raised when a message contains invalid data.

    Examples
    --------
    - empty message identifier;
    - missing payload;
    - invalid metadata;
    - malformed headers.

    """


class MessageSerializationError(MessagingError):
    """
    Raised when a message cannot be serialized.

    Examples
    --------
    - unsupported payload type;
    - JSON encoding failure;
    - protobuf encoding failure.

    """


class MessageDeserializationError(MessagingError):
    """
    Raised when a serialized message cannot be decoded.

    Examples
    --------
    - malformed JSON;
    - invalid protobuf message;
    - unsupported message format.

    """


class EnvelopeError(MessagingError):
    """
    Raised when a MessageEnvelope is invalid.

    Examples
    --------
    - missing metadata;
    - missing payload;
    - incompatible payload type.

    """


class MetadataError(MessagingError):
    """
    Raised when message metadata is invalid.

    Examples
    --------
    - invalid correlation identifier;
    - invalid causation identifier;
    - invalid timeout;
    - invalid timestamp.

    """


class HeaderError(MessagingError):
    """
    Raised when message headers are invalid.

    Examples
    --------
    - duplicate header;
    - invalid header name;
    - unsupported header value.

    """


__all__ = (
    "EnvelopeError",
    "HeaderError",
    "MessageDeserializationError",
    "MessageSerializationError",
    "MessageValidationError",
    "MessagingError",
    "MetadataError",
)
