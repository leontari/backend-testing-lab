"""Tests for messaging exceptions."""

from __future__ import annotations

import pytest

from shared.messaging.exceptions import (
    EnvelopeError,
    HeaderError,
    MessageDeserializationError,
    MessageSerializationError,
    MessageValidationError,
    MessagingError,
    MetadataError,
)


@pytest.mark.parametrize(
    ("exception_type",),
    [
        (MessageValidationError,),
        (MessageSerializationError,),
        (MessageDeserializationError,),
        (EnvelopeError,),
        (MetadataError,),
        (HeaderError,),
    ],
)
def test_all_exceptions_inherit_from_messaging_error(
    exception_type: type[Exception],
) -> None:
    """
    Every messaging exception must inherit MessagingError.
    """
    assert issubclass(exception_type, MessagingError)


@pytest.mark.parametrize(
    ("exception_type",),
    [
        (MessagingError,),
        (MessageValidationError,),
        (MessageSerializationError,),
        (MessageDeserializationError,),
        (EnvelopeError,),
        (MetadataError,),
        (HeaderError,),
    ],
)
def test_exception_message(exception_type: type[Exception]) -> None:
    """
    Exception should preserve message text.
    """
    message = "test message"
    exception = exception_type(message)

    assert str(exception) == message


def test_messaging_error_is_exception() -> None:
    """
    MessagingError must derive from Exception.
    """
    assert issubclass(MessagingError, Exception)
