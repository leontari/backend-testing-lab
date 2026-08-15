"""
Message headers.

Headers represent distributed context attached to a message.

They are serialized and propagated between services.

Responsibilities
----------------
- carry tracing context;
- carry transport-independent protocol information;
- carry application-defined distributed headers.

Headers are used by:
- HTTP adapters;
- Kafka adapters;
- gRPC adapters;
- CommandBus;
- EventBus;
- Workflow/Saga;
- Logger;
- Metrics;
- Tracing.

Important:
---------
Headers are NOT runtime metadata.

Use:
    MessageMetadata
for:
    - retry counters;
    - timestamps;
    - lifecycle state;
    - processing information.

Headers must remain transport-independent.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping


class HeaderKeys(StrEnum):
    """
    Standard infrastructure headers.

    These keys are owned by Runtime Kernel.
    Business-specific headers must NOT be added here.

    Example:
        headers.set("customer-id", "123")
    is valid.

    But:
        HeaderKeys.CUSTOMER_ID
    must not exist.

    """

    # W3C Trace Context
    TRACEPARENT = "traceparent"
    TRACESTATE = "tracestate"
    BAGGAGE = "baggage"

    # Common runtime context
    TENANT = "tenant"
    LOCALE = "locale"

    # Protocol information
    CONTENT_TYPE = "content-type"
    SCHEMA = "schema"

    # Message routing
    REPLY_TO = "reply-to"
    CORRELATION_ID = "correlation-id"


@dataclass(slots=True)
class MessageHeaders:
    """
    Distributed message headers container.

    Example:
    -------
        headers = MessageHeaders()
        headers.set(HeaderKeys.TRACEPARENT, traceparent)
        headers.set("customer-id", "123")

    Unknown keys are allowed intentionally.
    Kernel provides standard keys only.

    """

    _values: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate initial values."""
        for key, value in self._values.items():
            self._validate(key, value)

    @staticmethod
    def _validate(key: str, value: str) -> None:
        """Validate header entry."""
        if not isinstance(key, str):
            msg = "header key must be str"
            raise TypeError(msg)

        if not key:
            msg = "header key cannot be empty"
            raise ValueError(msg)

        if any(char.isspace() for char in key):
            msg = f"invalid header key: {key!r}"
            raise ValueError(msg)

        if not isinstance(value, str):
            msg = "header value must be str"
            raise TypeError(msg)

    def set(self, key: str | HeaderKeys, value: str) -> None:
        """Add or replace header."""
        self._validate(str(key), value)
        self._values[key] = value

    def get(
        self,
        key: str | HeaderKeys,
        default: str | None = None,
    ) -> str | None:
        """Get header value."""
        return self._values.get(str(key), default)

    def remove(self, key: str | HeaderKeys) -> None:
        """
        Remove header.

        Missing keys are ignored.

        """
        self._values.pop(str(key), None)

    def contains(self, key: str | HeaderKeys) -> bool:
        """Check header existence."""

        return str(key) in self._values

    def clear(self) -> None:
        """Remove all headers."""
        self._values.clear()

    def update(self, values: Mapping[str, str]) -> None:
        """Update headers from mapping."""
        for key, value in values.items():
            self.set(key, value)

    def copy(self) -> "MessageHeaders":
        """Create independent copy."""
        return MessageHeaders(_values=self._values.copy())

    @property
    def values(self) -> Mapping[str, str]:
        """
        Read-only view.

        Useful for:
        - serializers;
        - transport adapters.

        """
        return MappingProxyType(self._values)

    def __contains__(self, key: str | HeaderKeys) -> bool:
        return self.contains(key)

    def __getitem__(self, key: str | HeaderKeys) -> str:
        return self._values[str(key)]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)


__all__ = (
    "HeaderKeys",
    "MessageHeaders",
)
