"""
DTO serialization utilities.

Default implementation uses JSON.

Transport layers may replace this
implementation.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from shared.dto.exceptions import DTOSerializationError

if TYPE_CHECKING:
    from shared.dto.base import DTO


class DTOSerializer:
    """
    Serialize and deserialize DTO objects.

    Used by:
    - Kafka;
    - event bus;
    - HTTP adapters.
    """

    @staticmethod
    def dumps(dto: DTO) -> str:
        """
        Serialize DTO.

        Returns
        -------
        str
            JSON representation.

        """
        try:
            return json.dumps(dto.to_dict())
        except Exception as exc:
            msg = "DTO serialization failed"
            raise DTOSerializationError(msg) from exc

    @staticmethod
    def loads(payload: str, dto_type: type[DTO]) -> DTO:
        """
        Deserialize DTO.

        Parameters
        ----------
        payload:
            JSON payload.

        dto_type:
            DTO class.

        Returns
        -------
        DTO
            Restored DTO object.

        """
        try:
            data: dict[str, Any] = json.loads(payload)

            return dto_type(**data)

        except Exception as exc:
            msg = "DTO deserialization failed"
            raise DTOSerializationError(msg) from exc


__all__ = ("DTOSerializer",)
