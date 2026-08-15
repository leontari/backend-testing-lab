"""
Tests for runtime Message.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, dataclass

import pytest

from shared.messaging.identity import MessageIdentity
from shared.messaging.message import Message, MessageKind
from shared.messaging.metadata import MessageMetadata


@dataclass(slots=True, frozen=True)
class CreateOrder:
    order_id: int
    amount: float


def test_create_message() -> None:
    """
    Message stores all components.
    """
    payload = CreateOrder(order_id=10, amount=15.5)
    identity = MessageIdentity()
    metadata = MessageMetadata()

    message = Message(
        kind=MessageKind.COMMAND,
        payload=payload,
        identity=identity,
        metadata=metadata,
    )

    assert message.kind is MessageKind.COMMAND
    assert message.payload == payload
    assert message.identity == identity
    assert message.metadata == metadata


def test_message_is_frozen() -> None:
    """
    Message is immutable.
    """
    message = Message(
        kind=MessageKind.EVENT,
        payload=1,
        identity=MessageIdentity(),
        metadata=MessageMetadata(),
    )

    with pytest.raises(FrozenInstanceError):
        message.payload = 10  # type: ignore[misc]


def test_message_is_hashable() -> None:
    """
    Frozen messages should support hashing.

    This assumes MessageMetadata is hashable.
    """
    message = Message(
        kind=MessageKind.EVENT,
        payload=1,
        identity=MessageIdentity(),
        metadata=MessageMetadata(),
    )

    mapping = {
        message: "ok",
    }

    assert mapping[message] == "ok"


def test_message_equality() -> None:
    """
    Equality is value based.
    """
    identity = MessageIdentity()

    metadata = MessageMetadata()

    payload = CreateOrder(
        order_id=1,
        amount=2.5,
    )

    left = Message(
        kind=MessageKind.REQUEST,
        payload=payload,
        identity=identity,
        metadata=metadata,
    )

    right = Message(
        kind=MessageKind.REQUEST,
        payload=payload,
        identity=identity,
        metadata=metadata,
    )

    assert left == right


@pytest.mark.parametrize(
    "kind",
    [
        MessageKind.COMMAND,
        MessageKind.EVENT,
        MessageKind.REQUEST,
        MessageKind.RESPONSE,
    ],
)
def test_all_message_kinds(kind: MessageKind) -> None:
    """
    Every message kind can be instantiated.
    """
    message = Message(
        kind=kind,
        payload=object(),
        identity=MessageIdentity(),
        metadata=MessageMetadata(),
    )

    assert message.kind is kind


def test_generic_payload_type() -> None:
    """
    Message preserves payload type.
    """
    payload = CreateOrder(
        order_id=42,
        amount=100,
    )

    message = Message[CreateOrder](
        kind=MessageKind.COMMAND,
        payload=payload,
        identity=MessageIdentity(),
        metadata=MessageMetadata(),
    )

    assert isinstance(
        message.payload,
        CreateOrder,
    )


def test_message_kind_values() -> None:
    """
    MessageKind exposes stable serialization values.
    """
    assert MessageKind.COMMAND.value == "command"
    assert MessageKind.EVENT.value == "event"
    assert MessageKind.REQUEST.value == "request"
    assert MessageKind.RESPONSE.value == "response"
