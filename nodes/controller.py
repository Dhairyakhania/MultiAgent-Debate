def rounds_controller(state, logger=None):
    if logger:
        logger.log("controller_check", {
            "current_round": state["current_round"],
            "current_turn": state["current_turn"]
        })

    if state["current_turn"] not in ("AgentA", "AgentB"):
        raise RuntimeError(f"Invalid current_turn: {state['current_turn']}")

    return state
