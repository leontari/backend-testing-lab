"""Workflow execution context."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(slots=True)
class WorkflowContext:
    """
    Runtime workflow context.

    Stores:
    - workflow id;
    - current state;
    - business data.

    """

    id: UUID = field(default_factory=uuid4)
    data: dict[str, object] = field(default_factory=dict)
