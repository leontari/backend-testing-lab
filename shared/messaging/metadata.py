"""
Runtime message metadata.

Metadata contains runtime-only information associated with message
processing.

It is not serialized and never leaves the current runtime process.

Responsibilities:
- execution lifecycle;
- retry information;
- delivery diagnostics;
- transport runtime information.

Unlike MessageHeaders:
    headers -> distributed between services
    metadata -> local runtime only
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


class MetadataKeys(StrEnum):
    """Standard runtime metadata attribute keys."""

    TRANSPORT = "transport"
    TOPIC = "topic"
    PARTITION = "partition"
    OFFSET = "offset"
    CONSUMER_GROUP = "consumer_group"
    REMOTE_ADDRESS = "remote_address"
    WORKFLOW = "workflow"
    WORKFLOW_STEP = "workflow_step"
    SAGA = "saga"
    HTTP_METHOD = "http_method"
    HTTP_PATH = "http_path"
    GRPC_SERVICE = "grpc_service"
    GRPC_METHOD = "grpc_method"


class RuntimeStatus(StrEnum):
    """Message processing lifecycle state."""

    RECEIVED = "received"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


_ALLOWED_TRANSITIONS: dict[RuntimeStatus, frozenset[RuntimeStatus]] = {
    RuntimeStatus.RECEIVED: frozenset({RuntimeStatus.PROCESSING}),
    RuntimeStatus.PROCESSING: frozenset(
        {
            RuntimeStatus.COMPLETED,
            RuntimeStatus.FAILED,
            RuntimeStatus.RETRYING,
            RuntimeStatus.CANCELLED,
        }
    ),
    RuntimeStatus.RETRYING: frozenset({RuntimeStatus.PROCESSING}),
    RuntimeStatus.COMPLETED: frozenset(),
    RuntimeStatus.FAILED: frozenset(),
    RuntimeStatus.CANCELLED: frozenset(),
}


@dataclass(slots=True)
class MessageMetadata:
    """
    Runtime metadata attached to Message.

    Metadata is mutable because it represents message lifecycle.

    It must never be serialized.
    """

    received_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    processed_at: datetime | None = None
    status: RuntimeStatus = RuntimeStatus.RECEIVED
    transport: str | None = None
    deadline: timedelta | None = None
    priority: int = 0
    retry_count: int = 0
    delivery_attempt: int = 1
    attributes: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate metadata invariants."""
        if self.received_at.tzinfo is None:
            msg = "received_at must be timezone-aware"
            raise ValueError(msg)

        if self.processed_at is not None and self.processed_at.tzinfo is None:
            msg = "processed_at must be timezone-aware"
            raise ValueError(msg)

        if self.deadline is not None and self.deadline < timedelta(0):
            msg = "deadline cannot be negative"
            raise ValueError(msg)

        if self.retry_count < 0:
            msg = "retry_count cannot be negative"
            raise ValueError(msg)

        if self.delivery_attempt < 1:
            msg = "delivery_attempt must be greater than zero"
            raise ValueError(msg)

    def transition(self, new_status: RuntimeStatus) -> None:
        """
        Change lifecycle state.

        Raises
        ------
        RuntimeError
            If transition is invalid.

        """
        allowed = _ALLOWED_TRANSITIONS[self.status]

        if new_status not in allowed:
            msg = f"Invalid transition {self.status} -> {new_status}"
            raise RuntimeError(msg)

        self.status = new_status

    @property
    def is_completed(self) -> bool:
        """
        Whether message processing is finished successfully.

        Returns:
             True if processing finished successfully.

        """
        return self.status is RuntimeStatus.COMPLETED

    @property
    def is_terminal(self) -> bool:
        """
        Whether any sort of processing is no longer expected.

        Returns:
             True if no more processing is expected.

        """
        return self.status in {
            RuntimeStatus.COMPLETED,
            RuntimeStatus.FAILED,
            RuntimeStatus.CANCELLED,
        }

    def start_processing(self) -> None:
        """
        Move message into processing state.

        RECEIVED/RETRYING -> PROCESSING.
        """
        self.transition(RuntimeStatus.PROCESSING)

    def complete(self) -> None:
        """Mark processing as completed."""
        self.transition(RuntimeStatus.COMPLETED)
        self.processed_at = datetime.now(UTC)

    def fail(self) -> None:
        """
        Mark processing as failed.

        PROCESSING -> FAILED.
        """
        self.transition(RuntimeStatus.FAILED)
        self.processed_at = datetime.now(UTC)

    def retry(self) -> None:
        """
        Mark message for retry.

        PROCESSING -> RETRYING.
        """
        self.retry_count += 1
        self.delivery_attempt += 1
        self.transition(RuntimeStatus.RETRYING)

    def cancel(self) -> None:
        """
        Cancel message processing.

        PROCESSING -> CANCELLED.
        """
        self.transition(RuntimeStatus.CANCELLED)
        self.processed_at = datetime.now(UTC)

    def set(self, key: str, value: object) -> None:
        """Store custom runtime attribute."""
        self.attributes[key] = value

    def get(self, key: str, default: object | None = None) -> object | None:
        """
        Read custom runtime attribute.

        Returns:
            custom runtime attribute by key

        """
        return self.attributes.get(key, default)

    @property
    def readonly_attributes(self) -> Mapping[str, object]:
        """Read-only attributes view."""
        return MappingProxyType(self.attributes)


__all__ = (
    "MessageMetadata",
    "MetadataKeys",
    "RuntimeStatus",
)
