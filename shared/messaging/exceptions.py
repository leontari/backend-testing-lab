"""
Messaging exceptions.

Contains common exceptions for
message lifecycle and validation.
"""

from __future__ import annotations


class MessagingError(Exception):
    """Base messaging exception."""


class MessageValidationError(MessagingError):
    """Raised when message structure is invalid."""


class MessageTypeError(MessagingError):
    """Raised when message payload type is invalid."""
