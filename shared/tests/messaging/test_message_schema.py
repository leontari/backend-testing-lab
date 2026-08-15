"""
Tests for MessageSchema.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from dataclasses import dataclass

import pytest

from shared.messaging.message import MessageKind
from shared.messaging.message_schema import MessageSchema


@dataclass(slots=True, frozen=True)
class PaymentCreated:
    """
    Test DTO.
    """

    payment_id: str


def test_create_schema() -> None:
    """
    Schema stores all fields.
    """
    schema = MessageSchema(
        name="payment.created",
        version=1,
        kind=MessageKind.EVENT,
        payload_type=PaymentCreated,
    )

    assert schema.name == "payment.created"
    assert schema.version == 1
    assert schema.kind is MessageKind.EVENT
    assert schema.payload_type is PaymentCreated


def test_schema_is_frozen() -> None:
    """
    Schema is immutable.
    """
    schema = MessageSchema(
        name="payment.created",
        version=1,
        kind=MessageKind.EVENT,
        payload_type=PaymentCreated,
    )

    with pytest.raises(FrozenInstanceError):
        schema.version = 2  # type: ignore[misc]


@pytest.mark.parametrize(
    "name",
    [
        "",
        " ",
        "    ",
    ],
)
def test_empty_name(name: str) -> None:
    """
    Empty schema names are rejected.
    """
    with pytest.raises(ValueError):
        MessageSchema(
            name=name,
            version=1,
            kind=MessageKind.EVENT,
            payload_type=PaymentCreated,
        )


@pytest.mark.parametrize(
    "version",
    [
        0,
        -1,
        -100,
    ],
)
def test_invalid_version(version: int) -> None:
    """
    Schema version must be positive.
    """
    with pytest.raises(ValueError):
        MessageSchema(
            name="payment.created",
            version=version,
            kind=MessageKind.EVENT,
            payload_type=PaymentCreated,
        )


def test_schema_equality() -> None:
    """
    Equality is value-based.
    """
    left = MessageSchema(
        name="payment.created",
        version=1,
        kind=MessageKind.EVENT,
        payload_type=PaymentCreated,
    )

    right = MessageSchema(
        name="payment.created",
        version=1,
        kind=MessageKind.EVENT,
        payload_type=PaymentCreated,
    )

    assert left == right


def test_schema_hashable() -> None:
    """
    Frozen schema is hashable.
    """
    schema = MessageSchema(
        name="payment.created",
        version=1,
        kind=MessageKind.EVENT,
        payload_type=PaymentCreated,
    )

    mapping = {
        schema: "registered",
    }

    assert mapping[schema] == "registered"


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
    Every MessageKind is supported.
    """
    schema = MessageSchema(
        name="schema",
        version=1,
        kind=kind,
        payload_type=PaymentCreated,
    )

    assert schema.kind is kind
