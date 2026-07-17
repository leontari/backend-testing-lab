"""
Base DTO implementation.

Provides common functionality for all data transfer objects.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class DTO:
    """
    Base data transfer object.

    DTO objects are immutable data containers
    used for communication between application
    boundaries.

    Responsibilities:
    - store transport data;
    - provide serialization;
    - provide dictionary conversion.

    DTO does not:
    - contain business logic;
    - access database;
    - perform domain operations.

    """

    def to_dict(self) -> dict[str, Any]:
        """
        Convert DTO to dictionary.

        Returns
        -------
        dict[str, Any]
            Serializable representation.

        """
        return asdict(self)
