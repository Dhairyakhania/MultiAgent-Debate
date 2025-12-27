# Multi-Agent Debate DAG

## Overview

This project implements a **structured multi-agent debate system** using **LangGraph**.  
Two AI agents with distinct personas debate a user-provided topic in a strictly controlled, deterministic workflow.

The system enforces:
- Exact round limits
- Strict turn alternation
- Memory isolation
- Repetition detection with controlled retries
- Quantitative novelty scoring
- Objective judge evaluation
- Full execution logging
- CLI-only operation

All language generation is performed **locally using Ollama**, making the solution **fully open-source and offline-capable**.

---

## Key Design Decisions

### 1. Round Definition (Important)

A **round corresponds to a single agent turn**.

- Total rounds: **8**
- Turns per agent: **4**
- Order: `AgentA → AgentB → AgentA → …`
- Debate ends exactly after Round 8

This interpretation matches the assignment requirement:

> “Run exactly 8 rounds total (4 turns per agent, alternating).”

---

### 2. Agent Personas

- **AgentA (Scientist)**  
  Focuses on evidence, mechanisms, real-world impact, and technical reasoning.

- **AgentB (Philosopher)**  
  Focuses on societal implications, ethics, long-term consequences, and values.

Personas are externalized in a YAML config file for easy modification.

---

### 3. LangGraph DAG Architecture

The debate is implemented as a **state-driven DAG**, not a loop.

UserInput
↓
Controller ──→ AgentA ──→ Controller ──→ AgentB ──→ ...
↓
HardStop
↓
Judge
↓
END


**Why this matters**
- Prevents infinite loops
- Guarantees termination
- Makes control flow explicit and inspectable

---

### 4. State Management

All nodes operate on a shared `DebateState`:

```json
{
  "topic": "...",
  "current_round": 1,
  "current_turn": "AgentA",
  "turns": [],
  "violations": [],
  "judge_model": "mistral"
}
```

### 5. Memory Isolation

Each agent receives only:
    - The debate topic
    - The last two turns (sliding window)

This prevents:
    - Full-context repetition
    - Generic restatements
    - Prompt bloat

### 6. Repetition Detection & Retry Logic

To prevent repeated arguments:
    - A lightweight semantic repetition detector (word overlap–based) is applied
    - If repetition is detected:
        - The agent retries generation (up to 2 times)
        - Violations are logged

    - The debate never crashes due to repetition

This mirrors real-world agent orchestration systems.

### 7. Novelty Scoring (Per Round)

Each agent turn is assigned a novelty score:
    - Range: 0.0 → 1.0
    - Higher score = more novel contribution
    - Stored in state and logs

This enables objective evaluation beyond subjective judgment.

### 8. Judge Evaluation with Penalties
The JudgeNode:
    - Reviews the full transcript
    - Considers:
        - Argument quality
        - Logical progression
        - Average novelty score
        - Retry counts
        - Logged violations
    
    - Penalizes repeated or low-novelty agents
    - Produces:
        - Debate summary
        - Winner declaration
        - Reasoned justification

### 9. Logging (Full Traceability)

All events are logged to a single JSONL file with timestamps:
    - Agent inputs and outputs
    - Retry attempts
    - Repetition detections
    - Novelty scores
    - Judge statistics
    - Final verdict

This makes the system auditable and easy to debug.

### 10. Determinism

The system supports deterministic runs via:

    - Optional global random seed
    - Low-temperature generation
    - Controlled retry limits

Useful for testing, demos, and reproducible evaluation.

### Tech Stack

    - Python
    - LangGraph – workflow orchestration
    - Ollama – local LLM execution
    - Mistral / LLaMA-family models (via Ollama)
    - Graphviz – optional DAG visualization

No external APIs are used.

## Installation

### 1. Install Ollama

Download and install Ollama from:
```
https://ollama.com
```

Pull a model:
```
ollama pull mistral
```
(Ollama runs as a background service on Windows.)

### 2. Python Environment

```
pip install -r requirements.txt
```

### Running the Debate
Basic Run
```
python run_debate.py
```

With Options
```
python run_debate.py \
  --model mistral \
  --judge-model mistral \
  --seed 42 \
  --draw-dag \
  --log-path logs/debate_log.jsonl
```

## Conclusion

This project demonstrates:

    - Practical multi-agent orchestration
    - Strong control over LLM behavior
    - Careful handling of failure modes
    - Clear, inspectable system design