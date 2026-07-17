"""Saga workflow definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.workflow.context import WorkflowContext
    from shared.workflow.step import WorkflowStep


@dataclass(slots=True)
class Saga:
    """
    Sequential business workflow.

    Example:
        ReserveStock
              |
        ChargePayment
              |
        ShipOrder

    """

    steps: list[WorkflowStep] = field(default_factory=list)

    async def execute(self, context: WorkflowContext) -> None:
        """
        Execute saga steps.

        If step fails, compensating actions are executed.
        """
        completed: list[WorkflowStep] = []

        try:
            for step in self.steps:
                await step.execute(context)

                completed.append(step)

        except Exception:
            for step in reversed(completed):
                await step.compensate(context)

            raise
