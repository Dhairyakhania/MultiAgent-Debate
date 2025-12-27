import argparse
import yaml
from datetime import datetime
from langgraph.graph import StateGraph, END

from utils.state import DebateState
from utils.logger import DebateLogger
from utils.seed import set_global_seed
from utils.dag_visualizer import render_dag

from nodes.user_input import user_input_node
from nodes.controller import rounds_controller
from nodes.agent import agent_node_factory
from nodes.judge import judge_node
from nodes.hard_stop import hard_stop_node


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="mistral")
    parser.add_argument("--judge-model", default="mistral")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--draw-dag", action="store_true")
    parser.add_argument("--log-path")
    args = parser.parse_args()

    set_global_seed(args.seed)

    log_path = args.log_path or f"logs/debate_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
    logger = DebateLogger(log_path)

    topic = input("Enter topic for debate: ")

    with open("config/personas.yaml") as f:
        personas = yaml.safe_load(f)

    state: DebateState = {
        "topic": topic,
        "current_round": 1,
        "current_turn": "AgentA",
        "turns": [],
        "summary": "",
        "violations": [],
        "judge_model": args.judge_model,
    }

    graph = StateGraph(DebateState)

    graph.add_node("input", user_input_node)
    graph.add_node("controller", rounds_controller)

    graph.add_node(
        "agent_a",
        agent_node_factory("AgentA", personas["AgentA"], args.model, logger),
    )
    graph.add_node(
        "agent_b",
        agent_node_factory("AgentB", personas["AgentB"], args.model, logger),
    )

    graph.add_node("hard_stop", hard_stop_node)
    graph.add_node("judge", lambda s: judge_node(s, logger))

    graph.set_entry_point("input")
    graph.add_edge("input", "controller")

    def router(state):
        if state["current_round"] > 8:
            return "hard_stop"
        return "agent_a" if state["current_turn"] == "AgentA" else "agent_b"

    graph.add_conditional_edges("controller", router)
    graph.add_edge("agent_a", "controller")
    graph.add_edge("agent_b", "controller")
    graph.add_edge("hard_stop", "judge")
    graph.add_edge("judge", END)

    app = graph.compile()

    if args.draw_dag:
        render_dag(app)

    app.invoke(state)
    print(f"\nLogs saved to {log_path}")


if __name__ == "__main__":
    main()
