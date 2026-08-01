"""Workflow state definitions."""

from __future__ import annotations

from enum import Enum


class WorkflowStatus(Enum):
    """Persistent workflow status."""

    CREATED = "created"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
