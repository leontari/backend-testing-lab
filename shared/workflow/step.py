"""Workflow step abstraction."""

from __future__ import annotations

from typing import Protocol


class WorkflowStep(Protocol):
    """Single workflow execution step."""

    async def execute(self, context) -> None:
        """Execute step."""

    async def compensate(self, context) -> None:
        """
        Rollback step.

        Used by Saga pattern.
        """
