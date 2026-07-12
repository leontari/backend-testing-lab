from __future__ import annotations

import pytest

from shared.tracing.tracing import Tracing
from shared.tracing.manager import TraceManager


@pytest.fixture
def trace_manager():
    return TraceManager()


@pytest.fixture
def tracing():
    return Tracing()
