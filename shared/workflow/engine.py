"""Workflow engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from shared.workflow.exceptions import WorkflowNotFoundError

if TYPE_CHECKING:
    from shared.workflow.context import WorkflowContext
    from shared.workflow.saga import Saga


@dataclass(slots=True)
class WorkflowEngine:
    """
    Executes registered workflows.

    Responsibilities:
        - workflow registration;
        - workflow execution;
        - lifecycle tracking.

    """

    _workflows: dict[str, Saga] = field(default_factory=dict)

    def register(self, name: str, workflow: Saga) -> None:
        """Register workflow."""
        self._workflows[name] = workflow

    async def start(self, name: str, context: WorkflowContext) -> None:
        """
        Start workflow.

        Parameters
        ----------
        name:
            Workflow name.

        context:
            Workflow context.

        """
        workflow = self._workflows.get(name)

        if workflow is None:
            raise WorkflowNotFoundError(name)

        await workflow.execute(context)
