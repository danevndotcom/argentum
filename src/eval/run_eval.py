"""
Argentum Evaluation Runner – v0.2
Runs the current set of tasks and prints a summary.
"""

from pathlib import Path
import sys

# Make sure we can import from src
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.eval.tasks.task_01_create_ping import run_task as task_01
from src.eval.tasks.task_02_create_nested_file import run_task as task_02
from src.eval.tasks.task_03_fix_stale_config import run_task as task_03
from src.eval.tasks.task_04_deliberate_failure_recovery import run_task as task_04
from src.eval.tasks.task_05_multi_step_dependency import run_task as task_05


def main():
    print("\n" + "=" * 60)
    print("ARGENTUM EVALUATION  |  Baseline Suite (AAB-1 to AAB-5)")
    print("=" * 60 + "\n")

    tasks = [
        ("AAB-1: task_01_create_ping", task_01),
        ("AAB-2: task_02_create_nested_file", task_02),
        ("AAB-3: task_03_fix_stale_config", task_03),
        ("AAB-4: task_04_deliberate_failure_recovery", task_04),
        ("AAB-5: task_05_multi_step_dependency", task_05),
    ]

    results = []
    for name, fn in tasks:
        print(f"→ Running {name} ...")
        outcome = fn()
        results.append(outcome)
        status = "PASS" if outcome["success"] else "FAIL"
        recovery = "recovery used" if outcome.get("details", {}).get("recovery_used", False) else ""
        print(f"  {status}  (trace entries: {outcome['trace_length']}){f' [{recovery}]' if recovery else ''}")
        print()

    passed = sum(1 for r in results if r["success"])
    total = len(results)

    print("=" * 60)
    print(f"SUMMARY: {passed}/{total} tasks passed")
    print("=" * 60 + "\n")

    return results


if __name__ == "__main__":
    main()
