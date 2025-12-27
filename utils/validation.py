def detect_repetition(turns, new_text, threshold=0.4):
    """
    Detects semantic repetition using word overlap ratio.
    Returns True if repetition is detected.
    """
    new_words = set(new_text.lower().split())

    if not new_words:
        return False

    for t in turns:
        old_words = set(t["text"].lower().split())
        if not old_words:
            continue

        overlap_ratio = len(new_words & old_words) / max(len(new_words), 1)

        if overlap_ratio >= threshold:
            return True

    return False

def is_repetition(state, new_text):
    """
    Non-fatal repetition check.
    Used by agent retry logic.
    """
    return detect_repetition(state["turns"], new_text)

def novelty_score(turns, new_text):
    """
    Returns novelty score in [0,1].
    Higher means more novel compared to previous turns.
    """
    new_words = set(new_text.lower().split())
    if not new_words or not turns:
        return 1.0

    max_overlap = 0.0
    for t in turns:
        old_words = set(t["text"].lower().split())
        overlap = len(new_words & old_words) / max(len(new_words), 1)
        max_overlap = max(max_overlap, overlap)

    return round(1.0 - max_overlap, 3)