"""
Message identity.

This module defines immutable identifiers describing relationships
between messages in a distributed system.

Identity describes message origin and causality.
It is serialized and propagated between services.

MessageIdentity is transport-agnostic and is shared by:
- CommandBus
- EventBus
- Workflow Engine
- HTTP
- gRPC
- Kafka

It does not contain transport metadata, tracing information or payload.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from shared.messaging.exceptions import MessageValidationError


@dataclass(slots=True, frozen=True)
class MessageIdentity:
    """
    Immutable message identifiers.

    Parameters
    ----------
    message_id:
        Globally unique message identifier.
    correlation_id:
        Correlation identifier shared by the entire workflow or request.
    causation_id:
        Identifier of the message that directly caused this one.
        None indicates a root message.
    created_at:
        Message creation timestamp.

    Notes
    -----
    - Every message has a unique ``message_id``.
    - Every workflow/request shares the same ``correlation_id``.
    - ``causation_id`` links parent and child messages.
    - ``created_at`` is not equal to ``received_at``.

    """

    message_id: UUID = field(default_factory=uuid4)
    correlation_id: UUID = field(default_factory=uuid4)
    causation_id: UUID | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        """Validate identity values."""
        self._validate_uuid(self.message_id, "message_id")
        self._validate_uuid(self.correlation_id, "correlation_id")

        if self.causation_id is not None:
            self._validate_uuid(self.causation_id, "causation_id")

        if self.created_at.tzinfo is None:
            msg = "created_at must be timezone-aware"
            raise ValueError(msg)

    @staticmethod
    def _validate_uuid(value: UUID, field_name: str) -> None:
        """
        Validate UUID value.

        Parameters
        ----------
        value:
            UUID value.

        field_name:
            Field name used in the exception message.

        Raises
        ------
        MessageValidationError
            If value is not a UUID instance.

        """
        if not isinstance(value, UUID):
            msg = f"{field_name} must be UUID"
            raise MessageValidationError(msg)


__all__ = ("MessageIdentity",)
