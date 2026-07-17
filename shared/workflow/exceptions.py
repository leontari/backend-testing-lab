"""Workflow exceptions."""

from __future__ import annotations


class WorkflowError(Exception):
    """Base workflow exception."""


class WorkflowNotFoundError(WorkflowError):
    """Workflow is not registered."""


class WorkflowStateError(WorkflowError):
    """Invalid workflow state transition."""


class WorkflowExecutionError(WorkflowError):
    """Workflow execution failed."""
