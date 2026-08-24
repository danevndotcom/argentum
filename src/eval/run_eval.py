"""
Argentum Evaluation Runner – v0.1
Runs the current set of tasks and prints a summary.
"""

from pathlib import Path
import sys

# Make sure we can import from src
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.eval.tasks.task_01_create_ping import run_task as task_01


def main():
    print("\n" + "=" * 60)
    print("ARGENTUM EVALUATION  |  AAB-1 (seed)")
    print("=" * 60 + "\n")

    tasks = [
        ("task_01_create_ping", task_01),
    ]

    results = []
    for name, fn in tasks:
        print(f"→ Running {name} ...")
        outcome = fn()
        results.append(outcome)
        status = "PASS" if outcome["success"] else "FAIL"
        print(f"  {status}  (trace entries: {outcome['trace_length']})")
        print()

    passed = sum(1 for r in results if r["success"])
    total = len(results)

    print("=" * 60)
    print(f"SUMMARY: {passed}/{total} tasks passed")
    print("=" * 60 + "\n")

    return results


if __name__ == "__main__":
    main()
