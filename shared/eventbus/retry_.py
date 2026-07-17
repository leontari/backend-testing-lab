"""Event retry policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """
    Defines retry behaviour.

    Parameters
    ----------
    attempts:
        Maximum execution attempts.

    delay:
        Delay between retries in seconds.

    """

    attempts: int = 3
    delay: float = 0.1


__all__ = ("RetryPolicy",)
