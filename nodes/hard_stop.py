from langgraph.graph import END

def hard_stop_node(state):
    # This node intentionally does nothing
    # Reaching it means the debate is finished
    assert len(state["turns"]) == 8, (
        f"Expected 8 turns, got {len(state['turns'])}"
    )
    return state
