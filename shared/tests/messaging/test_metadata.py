"""
Tests for runtime message metadata.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from shared.messaging.metadata import (
    MessageMetadata,
    MetadataKeys,
    RuntimeStatus,
)


def test_metadata_default_values() -> None:
    """
    Metadata is created with valid defaults.
    """
    metadata = MessageMetadata()

    assert metadata.status is RuntimeStatus.RECEIVED
    assert metadata.transport is None
    assert metadata.deadline is None
    assert metadata.priority == 0
    assert metadata.retry_count == 0
    assert metadata.delivery_attempt == 1
    assert metadata.processed_at is None
    assert metadata.received_at.tzinfo is not None


def test_received_at_must_be_timezone_aware() -> None:
    """
    Naive datetime is forbidden.
    """
    with pytest.raises(ValueError):
        MessageMetadata(received_at=datetime.now())


def test_processed_at_must_be_timezone_aware() -> None:
    """
    Processed datetime must contain timezone.
    """
    with pytest.raises(ValueError):
        MessageMetadata(processed_at=datetime.now())


@pytest.mark.parametrize(
    "deadline",
    [timedelta(seconds=-1), timedelta(days=-1)],
)
def test_negative_deadline_is_invalid(deadline: timedelta) -> None:
    """
    Deadline cannot be negative.
    """
    with pytest.raises(ValueError):
        MessageMetadata(deadline=deadline)


@pytest.mark.parametrize("retry_count", [-1, -100])
def test_negative_retry_count_is_invalid(retry_count: int) -> None:
    """
    Retry counter cannot be negative.
    """
    with pytest.raises(ValueError):
        MessageMetadata(retry_count=retry_count)


@pytest.mark.parametrize("attempt", [0, -1])
def test_invalid_delivery_attempt(attempt: int) -> None:
    """
    Delivery attempt starts from one.
    """
    with pytest.raises(ValueError):
        MessageMetadata(delivery_attempt=attempt)


def test_start_processing_changes_status() -> None:
    """
    RECEIVED -> PROCESSING transition.
    """
    metadata = MessageMetadata()
    metadata.start_processing()

    assert metadata.status is RuntimeStatus.PROCESSING


def test_start_processing_twice_fails() -> None:
    """
    Processing cannot start twice.
    """
    metadata = MessageMetadata()
    metadata.start_processing()

    with pytest.raises(RuntimeError):
        metadata.start_processing()


def test_complete_processing() -> None:
    """
    PROCESSING -> COMPLETED transition.
    """
    metadata = MessageMetadata()
    metadata.start_processing()
    metadata.complete()

    assert metadata.status is RuntimeStatus.COMPLETED
    assert metadata.processed_at is not None
    assert metadata.is_completed is True
    assert metadata.is_terminal is True


def test_complete_without_processing_is_allowed() -> None:
    """
    Current implementation allows direct completion.

    This test documents current behaviour.
    """
    metadata = MessageMetadata()
    metadata.complete()

    assert metadata.status is RuntimeStatus.COMPLETED


def test_complete_twice_fails() -> None:
    """
    Terminal state cannot be completed again.
    """
    metadata = MessageMetadata()
    metadata.complete()

    with pytest.raises(RuntimeError):
        metadata.complete()


def test_fail_processing() -> None:
    """
    Processing can fail.
    """
    metadata = MessageMetadata()
    metadata.start_processing()
    metadata.fail()

    assert metadata.status is RuntimeStatus.FAILED
    assert metadata.processed_at is not None
    assert metadata.is_terminal is True


def test_retry_processing() -> None:
    """
    Retry increments counters.
    """
    metadata = MessageMetadata()
    metadata.start_processing()
    metadata.retry()

    assert metadata.status is RuntimeStatus.RETRYING
    assert metadata.retry_count == 1
    assert metadata.delivery_attempt == 2


def test_retry_finished_message_fails() -> None:
    """
    Terminal messages cannot retry.
    """
    metadata = MessageMetadata()
    metadata.complete()

    with pytest.raises(RuntimeError):
        metadata.retry()


def test_cancel_processing() -> None:
    """
    Message can be cancelled.
    """
    metadata = MessageMetadata()
    metadata.start_processing()
    metadata.cancel()

    assert metadata.status is RuntimeStatus.CANCELLED
    assert metadata.processed_at is not None
    assert metadata.is_terminal is True


def test_cancel_finished_message_fails() -> None:
    """
    Terminal message cannot be cancelled.
    """
    metadata = MessageMetadata()
    metadata.complete()

    with pytest.raises(RuntimeError):
        metadata.cancel()


def test_runtime_attributes() -> None:
    """
    Custom runtime attributes work.
    """

    metadata = MessageMetadata()
    metadata.set(MetadataKeys.TOPIC, "payments")

    assert metadata.get(MetadataKeys.TOPIC) == "payments"


def test_missing_attribute_returns_default() -> None:
    """
    Missing key returns default.
    """
    metadata = MessageMetadata()

    assert metadata.get("unknown", "default") == "default"


def test_readonly_attributes() -> None:
    """
    Attributes view is read-only.
    """
    metadata = MessageMetadata()

    metadata.set("key", "value")
    readonly = metadata.readonly_attributes

    assert readonly["key"] == "value"

    with pytest.raises(TypeError):
        readonly["key"] = "changed"  # type: ignore[index]


def test_metadata_keys_are_strings() -> None:
    """
    Metadata keys are string enums.
    """
    assert MetadataKeys.TOPIC.value == "topic"
    assert MetadataKeys.WORKFLOW_STEP.value == "workflow_step"


def test_runtime_status_values() -> None:
    """
    Runtime statuses are stable.
    """
    assert RuntimeStatus.RECEIVED.value == "received"
    assert RuntimeStatus.PROCESSING.value == "processing"
    assert RuntimeStatus.COMPLETED.value == "completed"
    assert RuntimeStatus.FAILED.value == "failed"
    assert RuntimeStatus.RETRYING.value == "retrying"
    assert RuntimeStatus.CANCELLED.value == "cancelled"
