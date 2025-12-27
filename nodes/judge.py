from utils.llms import OllamaLLM

def judge_node(state):
    llm = OllamaLLM(model=state["judge_model"], temperature=0.2)

    prompt = f"""
You are the judge of a structured AI debate.

Topic:
{state['topic']}

Transcript:
{state['turns']}

Violations:
{state['violations']}

Tasks:
1. Provide a concise debate summary
2. Declare a winner (AgentA or AgentB)
3. Give a logical justification

Output format:
Summary:
Winner:
Justification:
"""

    verdict = llm.generate(prompt, max_tokens=400)

    state["final_judgment"] = verdict

    print("\n[Judge]")
    print(verdict)

    return state
