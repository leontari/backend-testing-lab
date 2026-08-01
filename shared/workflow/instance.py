"""Workflow runtime instance."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from shared.workflow.state import WorkflowStatus


@dataclass(slots=True)
class WorkflowInstance:
    """
    Persistent workflow instance.

    Represents one business process execution.

    Example:
        Order #123 payment workflow

    """

    workflow_id: UUID = field(default_factory=uuid4)
    workflow_type: str = ""
    status: WorkflowStatus = WorkflowStatus.CREATED
    current_step: int = 0
    payload: dict[str, object] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
