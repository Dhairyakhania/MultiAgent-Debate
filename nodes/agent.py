from utils.llms import OllamaLLM
from utils.validation import is_repetition, novelty_score


def agent_node_factory(agent_name, persona_prompt, model, logger):
    llm = OllamaLLM(model=model)

    def agent_node(state):
        recent_turns = state["turns"][-2:]
        max_retries = 2
        attempt = 0

        while True:
            prompt = f"""
Persona:
{persona_prompt}

Debate Topic:
{state['topic']}

Recent debate context (DO NOT repeat or paraphrase):
{recent_turns}

Rules:
- Introduce ONE genuinely new argument
- Avoid ethics/bias/regulation unless adding a new angle
- Be concrete and analytical
- Minimum 5–7 sentences
- No summaries or conclusions

Argument:
"""

            logger.log("agent_attempt", {
                "agent": agent_name,
                "round": state["current_round"],
                "attempt": attempt + 1
            })

            response = llm.generate(prompt)

            if not is_repetition(state, response):
                break

            # Repetition detected → log + retry
            state["violations"].append(
                f"Repetition detected by {agent_name} in round {state['current_round']}"
            )

            logger.log("repetition_detected", {
                "agent": agent_name,
                "round": state["current_round"],
                "attempt": attempt + 1,
                "text": response
            })

            attempt += 1
            if attempt >= max_retries:
                # Accept last response to avoid deadlock
                break

        # ---- Novelty Scoring ----
        score = novelty_score(state["turns"], response)

        print(f"[Round {state['current_round']}] {agent_name}: {response}")

        state["turns"].append({
            "round": state["current_round"],
            "agent": agent_name,
            "text": response,
            "meta": {
                "retries": attempt,
                "novelty_score": score
            }
        })

        logger.log("agent_output", {
            "agent": agent_name,
            "round": state["current_round"],
            "retries": attempt,
            "novelty_score": score,
            "text": response
        })

        logger.log("novelty_score", {
            "agent": agent_name,
            "round": state["current_round"],
            "novelty_score": score
        })

        # Advance debate
        state["current_round"] += 1
        state["current_turn"] = "AgentB" if agent_name == "AgentA" else "AgentA"

        return state

    return agent_node
