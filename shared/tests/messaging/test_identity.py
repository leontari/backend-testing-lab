"""
Tests for MessageIdentity.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from shared.messaging.identity import MessageIdentity


def test_identity_generates_default_values() -> None:
    """
    Identity generates message and correlation ids.
    """

    identity = MessageIdentity()

    assert identity.message_id is not None
    assert identity.correlation_id is not None
    assert identity.causation_id is None

    assert isinstance(identity.created_at, datetime)


def test_message_id_is_unique() -> None:
    """
    Each identity has unique message id.
    """

    first = MessageIdentity()
    second = MessageIdentity()

    assert first.message_id != second.message_id


def test_correlation_id_can_be_shared() -> None:
    """
    Messages in one flow share correlation id.
    """

    correlation_id = uuid4()
    first = MessageIdentity(correlation_id=correlation_id)
    second = MessageIdentity(correlation_id=correlation_id)

    assert first.correlation_id == second.correlation_id


def test_causation_id_can_be_set() -> None:
    """
    Child message can reference parent message.
    """

    parent_id = uuid4()
    identity = MessageIdentity(causation_id=parent_id)

    assert identity.causation_id == parent_id


def test_created_at_requires_timezone() -> None:
    """
    created_at must be timezone-aware.
    """

    with pytest.raises(ValueError):
        MessageIdentity(created_at=datetime.now())


def test_created_at_accepts_utc() -> None:
    """
    UTC datetime is valid.
    """

    identity = MessageIdentity(created_at=datetime.now(UTC))

    assert identity.created_at.tzinfo is not None


def test_identity_is_immutable() -> None:
    """
    Identity is frozen.
    """

    identity = MessageIdentity()

    with pytest.raises(AttributeError):
        identity.message_id = uuid4()  # type: ignore[misc]
