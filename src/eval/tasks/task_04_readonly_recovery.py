"""
Task 04 – Recover from a read-only target file
Goal: Ensure locked.txt contains exactly unlocked

Setup writes locked.txt with stale content and makes it read-only (chmod 444).
The runtime's first write must fail. Recovery must chmod the file back to
writable, then rewrite. Tests that recover() performs a real corrective action.
"""

import os
import stat
from pathlib import Path
from typing import Optional, Dict, Any

from src.runtime.loop import ArgentumRuntime


def run_task(workspace: Optional[Path] = None) -> Dict[str, Any]:
    ws = workspace or Path.cwd()

    target = ws / "locked.txt"
    target.write_text("stale\n", encoding="utf-8")
    os.chmod(target, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

    runtime = ArgentumRuntime(workspace=workspace)
    goal = "Ensure locked.txt contains exactly unlocked"
    result = runtime.run(goal, target_path="locked.txt", target_content="unlocked")

    try:
        os.chmod(target, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass

    exists = target.exists()
    content_ok = False
    if exists:
        content_ok = target.read_text(encoding="utf-8").strip() == "unlocked"

    success = result.success and exists and content_ok

    return {
        "task_id": "task_04_readonly_recovery",
        "goal": goal,
        "success": success,
        "trace_length": len(result.trace),
        "details": {"file_exists": exists, "content_correct": content_ok},
    }


if __name__ == "__main__":
    print(run_task())
