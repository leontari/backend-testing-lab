"""
Message payload abstraction.

Payload represents business data transported inside Message.

Responsibilities:
- DTO metadata;
- schema identification;
- schema versioning;
- JSON-compatible representation.

Payload does not know about:
- HTTP;
- Kafka;
- gRPC;
- serialization transport.

Serialization is handled by serializers.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class Payload:
    """
    Generic message payload.

    Payload contains:

    schema:
        Stable message schema identifier.
    version:
        Schema version.
    data:
        Serialized DTO representation.

    Example:
        Payload(
            schema="payment.created",
            version=1,
            data={
                "payment_id": "123",
                "amount": 100,
            },
        )

    """

    schema: str
    version: int
    data: Mapping[str, Any]

    def __post_init__(self) -> None:
        """Validate payload contract."""
        if not self.schema:
            msg = "schema cannot be empty"
            raise ValueError(msg)

        if self.version < 1:
            msg = "version must be greater than zero"
            raise ValueError(msg)

        if not isinstance(self.data, Mapping):
            msg = "data must be mapping"
            raise TypeError(msg)

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-compatible representation."""
        return {
            "schema": self.schema,
            "version": self.version,
            "data": dict(self.data),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> Payload:
        """Create payload from dictionary.

        To be used by serializers.
        """
        return cls(
            schema=value["schema"],
            version=value["version"],
            data=value["data"],
        )


__all__ = ("Payload",)
