"""Workflow step abstraction."""

from __future__ import annotations

from typing import Protocol


class WorkflowStep(Protocol):
    """Saga step contract."""

    async def execute(self, context) -> None:
        """Execute step."""

    async def compensate(self, context) -> None:
        """
        Compensating action.

        Used by Saga pattern.
        """
