"""
Shared pytest fixtures.
"""

import pytest


@pytest.fixture
def sample_state():
    """
    Shared fake game state for tests.
    """

    return {
        "scenario": "test",
        "turn": 1,
        "nodes": [],
        "resources": {}
    }
