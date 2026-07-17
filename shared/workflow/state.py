"""Workflow state definitions."""

from __future__ import annotations

from enum import Enum


class WorkflowState(Enum):
    """Workflow lifecycle states."""

    CREATED = "created"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
