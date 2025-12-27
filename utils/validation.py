def detect_repetition(turns, new_text):
    for t in turns:
        if new_text.lower() in t["text"].lower():
            return True
    return False

def coherence_check(state, new_text):
    if detect_repetition(state["turns"], new_text):
        state["violations"].append("Repeated argument detected")
        raise RuntimeError("Repeated argument rejected")
