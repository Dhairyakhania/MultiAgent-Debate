from utils.validation import detect_repetition

def test_detects_clear_repetition():
    turns = [
        {"text": "AI systems can reinforce bias if trained on skewed data."}
    ]
    new_text = "AI systems may reinforce bias when trained on biased datasets."
    assert detect_repetition(turns, new_text) is True


def test_allows_novel_argument():
    turns = [
        {"text": "AI can automate repetitive coding tasks."}
    ]
    new_text = "AI changes how junior developers are trained and evaluated."
    assert detect_repetition(turns, new_text) is False
