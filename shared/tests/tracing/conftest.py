from __future__ import annotations

import pytest

from shared.tracing.factory import TraceFactory
from shared.tracing.manager import TraceManager


@pytest.fixture
def trace_manager():
    return TraceManager()


@pytest.fixture
def root_trace():
    return TraceFactory.create_root_trace()
