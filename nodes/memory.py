def update_memory(state, agent, text):
    state["turns"].append({
        "round": state["current_round"],
        "agent": agent,
        "text": text,
        "meta": {}
    })

    state["current_round"] += 1
    state["current_turn"] = "AgentB" if agent == "AgentA" else "AgentA"

    return state


def get_agent_memory(state, agent):
    opponent_turns = [
        t for t in state["turns"] if t["agent"] != agent
    ][-2:]

    return {
        "topic": state["topic"],
        "recent_opponent_turns": opponent_turns,
        "summary": state["summary"]
    }
