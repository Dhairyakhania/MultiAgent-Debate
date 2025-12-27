def rounds_controller(state):
    # Validate that current_turn is valid
    if state["current_turn"] not in ("AgentA", "AgentB"):
        raise RuntimeError(
            f"Invalid current_turn: {state['current_turn']}"
        )

    return state
