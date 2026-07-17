"""
Shared DTO framework.

Provides immutable transport contracts
for Runtime Kernel applications.
"""

from __future__ import annotations

from shared.dto.base import DTO
from shared.dto.registry import DTORegistry
from shared.dto.serializer import DTOSerializer
from shared.dto.version import DTOVersion

__all__ = (
    "DTO",
    "DTORegistry",
    "DTOSerializer",
    "DTOVersion",
)
