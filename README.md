# ARGENTUM

### An agentic execution runtime and evaluation harness for autonomous task completion.

> **Observe → Reason → Plan → Act → Verify → Recover**

Argentum is an experimental **agentic runtime** exploring a different approach to AI systems: designing around **autonomous execution**, rather than conversation alone.

**Important**: Argentum is not yet a language model. It is a real-code implementation of the agentic loop with deterministic baselines, verification mechanics, and recovery pathways. Model integration comes next.

## The idea

Most LLMs are designed primarily to generate useful responses.

Argentum explores what happens when the primary objective becomes:

**Take a goal. Execute it. Verify the result. Recover from failure.**

The loop is implemented as actual code, not prompt engineering.

## Architecture

```text
Goal
 ↓
Observe ──→ filesystem inspection
 ↓
Reason ──→ (currently deterministic, soon: LLM)
 ↓
Plan ────→ (currently deterministic, soon: LLM)
 ↓
Act ─────→ file operations
 ↓
Verify ──→ objective pass/fail check
 ↓
Recover ─→ error diagnosis + retry
 ↺
```

## Current Status

**Argentum v0.2 — Deterministic Baseline Complete**

✅ Real runtime loop in `src/runtime/loop.py`
✅ Five evaluation tasks (AAB-1 through AAB-5)
✅ Verification + recovery mechanics working
✅ 5/5 baseline tasks passing
✅ Public commit history showing real engineering progression

🔄 Next: Integrate open-weight LLM (Qwen2.5-Coder via Ollama) and measure what changes

## Evaluation Results

| Task ID | Name | Result | Recovery Used |
|---------|------|--------|---------------|
| AAB-1 | Create ping.txt | PASS | No |
| AAB-2 | Create nested file | PASS | Yes |
| AAB-3 | Fix stale config | PASS | No |
| AAB-4 | Deliberate failure | PASS | Yes |
| AAB-5 | Multi-step dependency | PASS | Yes |

**Summary: 5/5 tasks passed** — See [`RESULTS.md`](RESULTS.md) for full details.

## Repository Structure

```
argentum/
├── src/
│   ├── runtime/
│   │   └── loop.py          # OBSERVE→REASON→PLAN→ACT→VERIFY→RECOVER
│   ├── eval/
│   │   ├── run_eval.py      # Evaluation runner
│   │   └── tasks/           # AAB-1 through AAB-5
│   └── model/
│       └── __init__.py      # (empty — model integration next)
├── RESULTS.md               # Evaluation dashboard
├── README.md                # This file
├── LICENSE                  # MIT
└── SECURITY.md              # Security policy
```

## Philosophy

Argentum is not intended to compete with frontier general-purpose models on raw scale.

The research question is different:

> **Can an agentic runtime with verification and recovery make autonomous systems more reliable — regardless of the underlying model?**

The most valuable artifacts being built:
- The loop as code, not prompt theater
- Verification + recovery mechanics
- Benchmark tasks with objective pass/fail
- Public commit trail showing real engineering progression

## Roadmap

- [x] Build deterministic runtime loop
- [x] Create evaluation harness
- [x] Implement 5 baseline tasks (AAB-1 to AAB-5)
- [x] Document results in RESULTS.md
- [ ] Integrate Qwen2.5-Coder via Ollama
- [ ] Replace deterministic reason()/plan() with model calls
- [ ] Measure delta: deterministic vs model-driven
- [ ] Expand benchmark suite
- [ ] Publish build log

## How to Run

```bash
# Activate virtual environment
source .venv/bin/activate

# Run evaluation suite
python -m src.eval.run_eval
```

## Disclaimer

Argentum is an experimental research project. The current version uses deterministic rules for reasoning and planning. Model integration is the next milestone. Capabilities will evolve as the project develops.

---

*Built in public. Commit history is the resume.*
