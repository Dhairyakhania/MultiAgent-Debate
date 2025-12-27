import argparse
import yaml
from langgraph.graph import StateGraph, END

from utils.state import DebateState
from nodes.user_input import user_input_node
from nodes.controller import rounds_controller
from nodes.agent import agent_node_factory
from nodes.judge import judge_node
from nodes.hard_stop import hard_stop_node
from utils.dag_visualizer import render_dag


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="mistral")
    parser.add_argument("--judge-model", default="mistral")
    parser.add_argument("--log-path", default="debate_log.json")
    args = parser.parse_args()

    topic = input("Enter topic for debate: ")

    with open("config/personas.yaml") as f:
        personas = yaml.safe_load(f)

    # Initial state
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

    # Nodes
    graph.add_node("input", user_input_node)
    graph.add_node("controller", rounds_controller)

    graph.add_node(
        "agent_a",
        agent_node_factory("AgentA", personas["AgentA"], args.model),
    )
    graph.add_node(
        "agent_b",
        agent_node_factory("AgentB", personas["AgentB"], args.model),
    )

    graph.add_node("hard_stop", hard_stop_node)
    graph.add_node("judge", judge_node)

    # Entry
    graph.set_entry_point("input")

    # Edges
    graph.add_edge("input", "controller")

    def controller_router(state: DebateState):
        if state["current_round"] > 8:
            return "hard_stop"
        return "agent_a" if state["current_turn"] == "AgentA" else "agent_b"

    graph.add_conditional_edges("controller", controller_router)

    graph.add_edge("agent_a", "controller")
    graph.add_edge("agent_b", "controller")

    graph.add_edge("hard_stop", "judge")
    graph.add_edge("judge", END)

    app = graph.compile()

    # DAG rendering is optional
    render_dag(app)

    app.invoke(state)


if __name__ == "__main__":
    main()
