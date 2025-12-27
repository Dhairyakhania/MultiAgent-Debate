import pytest
from nodes.controller import rounds_controller

def test_out_of_turn():
    state = {
        "current_round": 1,
        "current_turn": "AgentB"
    }

    with pytest.raises(RuntimeError):
        rounds_controller(state)
