def judge_node(state, logger):
    from utils.llms import OllamaLLM

    llm = OllamaLLM(model=state["judge_model"], temperature=0.1)

    # Aggregate stats
    stats = {"AgentA": [], "AgentB": []}
    retries = {"AgentA": 0, "AgentB": 0}

    for t in state["turns"]:
        stats[t["agent"]].append(t["meta"].get("novelty_score", 0))
        retries[t["agent"]] += t["meta"].get("retries", 0)

    avg_novelty = {
        k: round(sum(v) / max(len(v), 1), 3)
        for k, v in stats.items()
    }

    logger.log("judge_stats", {
        "average_novelty": avg_novelty,
        "retries": retries,
        "violations": state["violations"]
    })

    prompt = f"""
You are the judge of a structured AI debate.

Topic:
{state['topic']}

Transcript:
{state['turns']}

Agent Metrics:
Average Novelty Scores: {avg_novelty}
Retry Counts (lower is better): {retries}
Violations: {state['violations']}

Judging Rules:
- Prefer agents with higher novelty
- Penalize repeated or recycled arguments
- Reward depth, clarity, and progression

Output Format:
Summary:
Winner:
Justification:
"""

    verdict = llm.generate(prompt, max_tokens=450)

    logger.log("judge_output", {"verdict": verdict})

    print("\n[Judge]")
    print(verdict)

    state["final_judgment"] = verdict
    return state
