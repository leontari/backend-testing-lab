"""
DTO registry.

Provides mapping between transport identifiers and DTO classes.

Used by:
- Kafka consumers;
- event bus;
- message dispatchers.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shared.dto.exceptions import DTORegistrationError

if TYPE_CHECKING:
    from shared.dto.base import DTO


@dataclass(slots=True)
class DTORegistry:
    """
    Runtime DTO type registry.

    Resolves DTO classes by:
        (name, version)

    Example:
        payment.created:v1
              |
              v
        PaymentCreatedDTO

    """

    _items: dict[tuple[str, int], type[DTO]]

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._items = {}

    def register(
        self,
        name: str,
        version: int,
        dto_type: type[DTO],
    ) -> None:
        """
        Register DTO type.

        Parameters
        ----------
        name:
            Transport DTO name.

        version:
            Schema version.

        dto_type:
            DTO implementation class.

        Raises
        ------
        DTORegistrationError
            If DTO already registered.

        """
        key = name, version

        if key in self._items:
            msg = f"DTO already registered: {key}"
            raise DTORegistrationError(msg)

        self._items[key] = dto_type

    def resolve(
        self,
        name: str,
        version: int,
    ) -> type[DTO]:
        """
        Resolve DTO class.

        Parameters
        ----------
        name:
            DTO name.

        version:
            DTO version.

        Returns
        -------
        type[DTO]
            Registered DTO class.

        """
        return self._items[name, version]


__all__ = ("DTORegistry",)
