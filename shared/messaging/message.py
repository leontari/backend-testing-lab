"""
Universal runtime message envelope.

Message is the central communication abstraction
between application components.

It is used by:
- HTTP
- Kafka
- gRPC
- CommandBus
- EventBus
- Workflow
- Saga

Message contains:
- identity
- headers
- metadata
- payload
- semantic kind

Message itself contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

from shared.messaging.headers import MessageHeaders
from shared.messaging.identity import MessageIdentity
from shared.messaging.metadata import MessageMetadata

if TYPE_CHECKING:
    from shared.messaging.payload import Payload


class MessageKind(StrEnum):
    """
    Message semantic type.

    Kind describes message intention, not transport.

    Command:
        Executes business logic.
    Event:
        Broadcasts something that has already happened.
    Request:
        Requires a response.
    Response:
        Replies to a previous request.
    """

    COMMAND = "command"
    EVENT = "event"
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"


@dataclass(slots=True, frozen=True)
class Message:
    """
    Universal message envelope.

    Parameters
    ----------
    kind:
        Semantic message kind.
    payload:
        Business DTO.
    identity:
        Immutable message identifiers.
    metadata:
        Immutable technical metadata.

    Example
    -------
    command = Message(
        kind=MessageKind.COMMAND,
        payload=CreateOrder(...),
    )

    Notes
    -----
    The payload type is intentionally unrestricted.
    The runtime accepts any DTO implementation:
    - dataclass
    - attrs
    - pydantic
    - protobuf
    - custom objects

    """

    kind: MessageKind
    payload: Payload
    identity: MessageIdentity = field(default_factory=MessageIdentity)
    headers: MessageHeaders = field(default_factory=MessageHeaders)
    metadata: MessageMetadata = field(default_factory=MessageMetadata)

    def __post_init__(self) -> None:
        """Validate message invariants."""
        if not isinstance(self.kind, MessageKind):
            msg = "kind must be MessageKind"
            raise TypeError(msg)

        if self.payload is None:
            msg = "payload cannot be None"
            raise ValueError(msg)

    @property
    def message_id(self) -> str:
        """Shortcut for identity id."""
        return str(self.identity.message_id)

    def is_command(self) -> bool:
        """Check command message."""
        return self.kind is MessageKind.COMMAND

    def is_event(self) -> bool:
        """Check event message."""
        return self.kind is MessageKind.EVENT

    def is_request(self) -> bool:
        """Check request message."""
        return self.kind is MessageKind.REQUEST

    def is_response(self) -> bool:
        """Check response message."""
        return self.kind is MessageKind.RESPONSE

    def is_notification(self) -> bool:
        """Check notification message."""
        return self.kind is MessageKind.NOTIFICATION


__all__ = (
    "Message",
    "MessageKind",
)
