from typing import TypedDict, List, Dict, Any

class DebateTurn(TypedDict):
    round: int
    agent: str
    text: str
    meta: Dict[str, Any]

class DebateState(TypedDict):
    topic: str
    current_round: int
    current_turn: str
    turns: List[DebateTurn]
    summary: str
    violations: List[str]
    judge_model: str
