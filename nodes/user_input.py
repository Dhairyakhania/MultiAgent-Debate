def user_input_node(state):
    topic = state["topic"].strip()

    if not (10 <= len(topic) <= 200):
        raise ValueError("Topic must be between 10 and 200 characters")

    state["topic"] = topic
    return state
