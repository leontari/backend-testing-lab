"""
Message serialization.

Converts Message objects into transport-neutral representations.

Supported formats:
- dict
- JSON string
- bytes

Serializer is independent of:
- HTTP
- Kafka
- gRPC

Runtime metadata is intentionally NOT serialized.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from . import MessageSerializationError
from .headers import MessageHeaders
from .identity import MessageIdentity
from .message import Message, MessageKind
from .payload import Payload

if TYPE_CHECKING:
    from collections.abc import Mapping


class MessageSerializer:
    """
    Default JSON message serializer.

    Converts:
        Message -> dict -> JSON -> bytes

    """

    def to_dict(self, message: Message) -> dict[str, Any]:
        """
        Convert Message to dictionary.

        Returns:
            Result is JSON-compatible dict.

        """
        try:
            return {
                "identity": {"message_id": message.identity.message_id},
                "kind": message.kind.value,
                "headers": dict(message.headers.values),
                "payload": message.payload.to_dict(),
            }

        except Exception as exc:
            msg = "Failed to serialize message"
            raise MessageSerializationError(msg) from exc

    def from_dict(self, value: Mapping[str, Any]) -> Message:
        """
        Restore Message from dictionary.

        Returns:
            Metadata recreated locally.

        """
        try:
            identity_data = value["identity"]
            identity = MessageIdentity(
                message_id=UUID(identity_data["message_id"]),
                correlation_id=UUID(identity_data["correlation_id"]),
                causation_id=(
                    UUID(identity_data["causation_id"])
                    if identity_data.get("causation_id")
                    else None
                ),
                created_at=datetime.fromisoformat(identity_data["created_at"]),
            )
            headers = MessageHeaders(_values=dict(value.get("headers", {})))
            payload = Payload.from_dict(value["payload"])

            return Message(
                kind=MessageKind(value["kind"]),
                payload=payload,
                headers=headers,
                identity=identity,
            )

        except Exception as exc:
            msg = "Failed to deserialize message"
            raise MessageSerializationError(msg) from exc

    def dumps(self, message: Message) -> str:
        """Serialize Message into JSON string."""
        return json.dumps(
            self.to_dict(message),
            ensure_ascii=False,
            separators=(",", ":"),
        )

    def loads(self, value: str) -> Message:
        """Deserialize Message from JSON string."""
        try:
            data = json.loads(value)
        except json.JSONDecodeError as exc:
            msg = "Invalid JSON message"
            raise MessageSerializationError(msg) from exc

        return self.from_dict(data)

    def dumps_bytes(self, message: Message) -> bytes:
        """
        Serialize Message into UTF-8 bytes.

        Useful for:
        - Kafka
        - gRPC

        Returns:
            message representation in bytes

        """
        return self.dumps(message).encode("utf-8")

    def loads_bytes(self, value: bytes) -> Message:
        """Deserialize Message from bytes."""
        return self.loads(value.decode("utf-8"))


__all__ = ("MessageSerializer",)
