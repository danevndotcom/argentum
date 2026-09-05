"""
Task 03 – Fix a stale file
Goal: Ensure config.txt contains exactly "v0.1"
Success criteria: file exists and content == "v0.1"

Unlike task_01/task_02, this task starts from a workspace where config.txt
already exists but holds the WRONG content ("v0.0"). It tests whether the
runtime correctly corrects existing-but-incorrect state, not just creates
missing files. Should pass without needing Recover.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from src.runtime.loop import ArgentumRuntime


def run_task(workspace: Optional[Path] = None) -> Dict[str, Any]:
    ws = workspace or Path.cwd()

    # Seed a deliberately wrong starting state before the runtime touches it.
    stale = ws / "config.txt"
    stale.write_text("v0.0\n", encoding="utf-8")

    runtime = ArgentumRuntime(workspace=workspace)
    goal = "Ensure config.txt contains exactly v0.1"
    result = runtime.run(goal, target_path="config.txt", target_content="v0.1")

    target = ws / "config.txt"
    exists = target.exists()
    content_ok = False
    if exists:
        content_ok = target.read_text(encoding="utf-8").strip() == "v0.1"

    success = result.success and exists and content_ok

    return {
        "task_id": "task_03_fix_stale_config",
        "goal": goal,
        "success": success,
        "trace_length": len(result.trace),
        "details": {
            "file_exists": exists,
            "content_correct": content_ok,
        },
    }


if __name__ == "__main__":
    outcome = run_task()
    print(outcome)
