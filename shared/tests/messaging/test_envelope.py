"""
Tests for MessageEnvelope.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone

import pytest

from shared.messaging.envelope import MessageEnvelope
from shared.messaging.identity import MessageIdentity
from shared.messaging.message import Message
from shared.messaging.message import MessageKind
from shared.messaging.metadata import MessageMetadata


@dataclass(slots=True, frozen=True)
class PaymentDTO:
    """
    Example business DTO.
    """

    payment_id: str
    amount: float


def create_message() -> Message[PaymentDTO]:
    """
    Create test message.
    """

    return Message(
        kind=MessageKind.COMMAND,
        payload=PaymentDTO(
            payment_id="p-1",
            amount=100,
        ),
        identity=MessageIdentity(),
        metadata=MessageMetadata(),
    )


def test_create_envelope() -> None:
    """
    Envelope stores message.
    """

    message = create_message()

    envelope = MessageEnvelope(
        message=message,
    )

    assert envelope.message == message
    assert envelope.trace is None
    assert isinstance(
        envelope.created_at,
        datetime,
    )


def test_created_at_is_utc() -> None:
    """
    Envelope timestamp is timezone aware.
    """

    envelope = MessageEnvelope(
        message=create_message(),
    )

    assert envelope.created_at.tzinfo == timezone.utc


def test_created_at_is_generated_per_instance() -> None:
    """
    Each envelope gets own timestamp.
    """

    first = MessageEnvelope(
        message=create_message(),
    )

    second = MessageEnvelope(
        message=create_message(),
    )

    assert first.created_at <= second.created_at


def test_envelope_is_frozen() -> None:
    """
    Envelope is immutable.
    """

    envelope = MessageEnvelope(
        message=create_message(),
    )

    with pytest.raises(FrozenInstanceError):
        envelope.trace = object()  # type: ignore[misc]


def test_envelope_equality() -> None:
    """
    Envelope equality is value based.
    """

    message = create_message()

    timestamp = datetime.now(timezone.utc)

    first = MessageEnvelope(
        message=message,
        created_at=timestamp,
    )

    second = MessageEnvelope(
        message=message,
        created_at=timestamp,
    )

    assert first == second
