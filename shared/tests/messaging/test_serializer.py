"""
Tests for MessageSerializer.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from shared.messaging.headers import (
    HeaderKeys,
    MessageHeaders,
)
from shared.messaging.identity import MessageIdentity
from shared.messaging.message import (
    Message,
    MessageKind,
)
from shared.messaging.payload import Payload
from shared.messaging.serializer import MessageSerializer


@pytest.fixture
def serializer() -> MessageSerializer:
    return MessageSerializer()


@pytest.fixture
def identity() -> MessageIdentity:
    return MessageIdentity(correlation_id=uuid4())


@pytest.fixture
def message(identity: MessageIdentity) -> Message:
    """
    Test message fixture.
    """

    headers = MessageHeaders()
    headers.set(HeaderKeys.TRACEPARENT, "00-test-trace")
    headers.set("customer-id", "123")
    payload = Payload(
        schema="payment.created",
        version=1,
        data={
            "payment_id": "pay-1",
            "amount": 100,
        },
    )

    return Message(
        kind=MessageKind.EVENT,
        payload=payload,
        identity=identity,
        headers=headers,
    )


def test_message_to_dict(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Message is converted to dict.
    """

    result = serializer.to_dict(message)

    assert result["kind"] == "event"
    assert result["headers"]["traceparent"] == "00-test-trace"
    assert result["payload"]["schema"] == "payment.created"


def test_identity_is_serialized(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Full identity is serialized.
    """

    result = serializer.to_dict(message)
    identity = result["identity"]

    assert "message_id" in identity
    assert "correlation_id" in identity
    assert "created_at" in identity


def test_message_json_roundtrip(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Message survives JSON roundtrip.
    """

    raw = serializer.dumps(
        message,
    )

    restored = serializer.loads(
        raw,
    )

    assert (
        restored.kind
        == MessageKind.EVENT
    )

    assert (
        restored.payload.schema
        == "payment.created"
    )

    assert (
        restored.payload.data["amount"]
        == 100
    )


def test_identity_survives_roundtrip(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Identity survives serialization.
    """

    restored = serializer.loads(
        serializer.dumps(message),
    )

    assert (
        restored.identity.message_id
        == message.identity.message_id
    )

    assert (
        restored.identity.correlation_id
        == message.identity.correlation_id
    )


def test_headers_survive_roundtrip(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Headers survive serialization.
    """

    restored = serializer.loads(
        serializer.dumps(message),
    )

    assert (
        restored.headers.get(
            HeaderKeys.TRACEPARENT,
        )
        == "00-test-trace"
    )

    assert (
        restored.headers.get(
            "customer-id",
        )
        == "123"
    )


def test_metadata_is_not_serialized(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Runtime metadata does not cross boundaries.
    """

    message.metadata.start_processing()

    data = serializer.to_dict(
        message,
    )

    assert (
        "metadata"
        not in data
    )


def test_bytes_roundtrip(
    serializer: MessageSerializer,
    message: Message,
) -> None:
    """
    Bytes serialization works.
    """

    raw = serializer.dumps_bytes(
        message,
    )

    restored = serializer.loads_bytes(
        raw,
    )

    assert (
        restored.payload.schema
        == message.payload.schema
    )


def test_invalid_json(
    serializer: MessageSerializer,
) -> None:
    """
    Invalid JSON raises error.
    """

    with pytest.raises(
        MessageSerializationError,
    ):
        serializer.loads(
            "{invalid",
        )


def test_invalid_payload_fails(
    serializer: MessageSerializer,
) -> None:
    """
    Missing payload raises error.
    """

    with pytest.raises(
        MessageSerializationError,
    ):
        serializer.from_dict(
            {
                "kind": "event",
                "identity": {},
            }
        )
