"""Workflow event correlation."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Correlation:
    """Event correlation data."""

    workflow_type: str
    key: str
