"""EventBus lifecycle."""

from __future__ import annotations

from enum import Enum


class EventBusState(Enum):
    CREATED = "created"
    RUNNING = "running"
    CLOSED = "closed"
