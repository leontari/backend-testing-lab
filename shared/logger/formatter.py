"""Structured JSON formatter."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

from shared.logger.context import current_context


class JsonFormatter(logging.Formatter):
    """
    JSON formatter for Kubernetes logging.

    Output is compatible with:
    - Loki
    - Elasticsearch
    - OpenSearch

    """

    def __init__(self, metadata: dict[str, object]) -> None:
        super().__init__()
        self._metadata = metadata

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            **self._metadata,
            **current_context().fields,
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            exc_type, exc, _ = record.exc_info
            payload.update(
                {
                    "error.type": exc_type.__name__ if exc_type else None,
                    "error.message": str(exc),
                }
            )

        return json.dumps(payload, ensure_ascii=False)


__all__ = ("JsonFormatter",)
