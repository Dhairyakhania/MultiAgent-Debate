from utils.llms import OllamaLLM
from utils.validation import coherence_check

def agent_node_factory(agent_name, persona_prompt, model_name):
    llm = OllamaLLM(model=model_name)

    def agent_node(state):
        prompt = f"""
You are participating in a structured debate.

Persona:
{persona_prompt}

Debate Topic:
{state['topic']}

Previous turns:
{state['turns']}

Rules:
- Produce ONE new argument
- Do NOT repeat previous arguments
- Stay on topic
- Be concise

Argument:
"""

        response = llm.generate(prompt)
        coherence_check(state, response)

        # Log + store turn
        print(f"[Round {state['current_round']}] {agent_name}: {response}")

        state["turns"].append({
            "round": state["current_round"],
            "agent": agent_name,
            "text": response,
            "meta": {}
        })

        # 🔁 Turn logic
        # if agent_name == "AgentA":
        #     # Same round, switch to AgentB
        #     state["current_turn"] = "AgentB"
        # else:
        #     # AgentB ends the round
        #     state["current_turn"] = "AgentA"
        #     state["current_round"] += 1

        # return state
        state["current_round"] += 1
        state["current_turn"] = "AgentB" if agent_name == "AgentA" else "AgentA"

        return state


    return agent_node
