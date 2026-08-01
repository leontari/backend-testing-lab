"""Workflow execution context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.workflow.instance import WorkflowInstance


@dataclass(slots=True)
class WorkflowContext:
    """
    Runtime workflow context.

    Wraps persistent instance.

    """

    instance: WorkflowInstance

    @property
    def data(self):
        """Workflow payload shortcut."""
        return self.instance.payload
