"""Workflow state storage abstraction."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from uuid import UUID

    from shared.workflow.instance import WorkflowInstance


class WorkflowStore(Protocol):
    """Workflow persistence interface."""

    async def save(self, instance: WorkflowInstance) -> None:
        """Save workflow state."""

    async def get(self, workflow_id: UUID) -> WorkflowInstance | None:
        """Load workflow state."""
