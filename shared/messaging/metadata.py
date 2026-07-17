"""
Message metadata.

Metadata contains transport-independent information required for:
    - message routing;
    - tracing;
    - diagnostics.

"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class MessageMetadata:
    """
    Immutable message metadata.

    Contains technical information, not business data.

    Fields
    ------
    message_id:
        Unique message identifier.
    created_at:
        Message creation timestamp.
    correlation_id:
        Identifier used to correlate related messages.
    causation_id:
        Identifier of message that caused current message.

    """

    message_id: UUID
    created_at: datetime
    correlation_id: UUID
    causation_id: UUID | None = None


def create_metadata(
    *,
    correlation_id: UUID | None = None,
    causation_id: UUID | None = None,
) -> MessageMetadata:
    """
    Create message metadata.

    Parameters
    ----------
    correlation_id:
        Existing operation correlation id.
    causation_id:
        Parent message id.

    Returns
    -------
    MessageMetadata
        Initialized metadata.

    """
    now = datetime.now(UTC)

    return MessageMetadata(
        message_id=uuid4(),
        created_at=now,
        correlation_id=correlation_id or uuid4(),
        causation_id=causation_id,
    )


__all__ = (
    "MessageMetadata",
    "create_metadata",
)
