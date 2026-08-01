"""Workflow engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from shared.workflow.context import WorkflowContext
from shared.workflow.instance import WorkflowInstance
from shared.workflow.state import WorkflowStatus

if TYPE_CHECKING:
    from shared.workflow.saga import Saga
    from shared.workflow.store import WorkflowStore


@dataclass(slots=True)
class WorkflowEngine:
    """
    Persistent Saga engine.

    Responsibilities:
        - create workflow instance;
        - execute steps;
        - save state;
        - resume workflow.

    """

    _store: WorkflowStore
    _workflows: dict[str, Saga] = field(default_factory=dict)

    def register(self, name: str, saga: Saga) -> None:
        """Register workflow."""
        self._workflows[name] = saga

    async def start(
        self,
        workflow_type: str,
        payload: dict[str, object],
    ) -> WorkflowInstance:
        """
        Start workflow.

        Returns
        -------
        WorkflowInstance
            Created workflow.

        """
        instance = WorkflowInstance(
            workflow_type=workflow_type,
            payload=payload,
        )
        await self._store.save(instance)
        await self.resume(instance)

        return instance

    async def resume(self, instance: WorkflowInstance) -> None:
        saga = self._workflows[instance.workflow_type]
        context = WorkflowContext(instance)

        instance.status = WorkflowStatus.RUNNING
        await self._store.save(instance)
        await saga.execute(context)
