"""
Tests for MessagePayload.
"""

from dataclasses import FrozenInstanceError

import pytest

from shared.messaging.payload import (
    MessagePayload,
)


def test_payload_content() -> None:

    payload = MessagePayload(
        content={"id": 1},
    )

    assert payload.content == {"id": 1}


def test_payload_is_generic() -> None:

    payload = MessagePayload[int](1)

    assert payload.content == 1


def test_payload_is_frozen() -> None:

    payload = MessagePayload(
        content=10,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        payload.content = 20


def test_payload_hashable() -> None:

    payload = MessagePayload(1)

    mapping = {
        payload: "ok",
    }

    assert mapping[payload] == "ok"


def test_payload_equality() -> None:

    left = MessagePayload(1)

    right = MessagePayload(1)

    assert left == right
