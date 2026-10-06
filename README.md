# Argentum

An experimental execution runtime and evaluation harness for autonomous agents.

> **Thesis:** Most LLMs are optimized to generate the next token. Argentum investigates execution architecture designed around completing a goal:  
> 

---

## 📊 Benchmark Suite (Argentum Agentic Benchmark - AAB)

Deterministic baselines established before introducing model-driven reasoning.

| Task | Description | Status | Recovery Triggered |
|---|---|:---:|:---:|
| **AAB-1** | Basic file creation & exact content verification | ✅ PASS | No |
| **AAB-2** | Nested directory creation & path handling | ✅ PASS | Yes (Directory repair) |
| **AAB-3** | Inspect and update stale configuration state | ✅ PASS | No |
| **AAB-4** | Permission lock & read-only error recovery | ✅ PASS | Yes (Permission reset) |
| **AAB-5** | Multi-step dependent execution | ⏳ Up Next | — |

---

## 🛠 Execution Architecture

Argentum implements its control flow as typed Python functions rather than prompt instructions:

```
[OBSERVE] -> Inspects actual workspace filesystem
[REASON]  -> Interprets explicit goal requirements
[PLAN]    -> Builds sequential execution strategy
[ACT]     -> Performs filesystem operations
[VERIFY]  -> Validates target state against ground truth
[RECOVER] -> Catches failure state and executes repairs
```

## 🚀 Running the Evaluation Suite

```bash
source .venv/bin/activate
python -m src.eval.run_eval
```
