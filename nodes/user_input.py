def user_input_node(state):
    topic = state["topic"].strip()
    if not (10 <= len(topic) <= 200):
        raise ValueError("Topic length must be 10–200 characters")
    return state
