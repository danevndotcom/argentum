"""
Task 02 – Create a nested file (exercises Recover for real)
Goal: Create sandbox/status.txt containing exactly "ready"
Success criteria: file exists and content == "ready"

This task deliberately targets a path whose parent directory does not exist
yet. The first ACT attempt fails — you can't write into a directory that
isn't there — which forces a genuine RECOVER step (create the directory)
before the retry can succeed. This is the first task where Recover does
something, not just exists as a label.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import shutil

from src.runtime.loop import ArgentumRuntime


def run_task(workspace: Optional[Path] = None) -> Dict[str, Any]:
    ws = workspace or Path.cwd()

    # Start from a clean state each time this task runs, so the recovery
    # path is genuinely exercised on every run rather than only the first.
    sandbox = ws / "sandbox"
    if sandbox.exists():
        shutil.rmtree(sandbox)

    runtime = ArgentumRuntime(workspace=workspace)
    goal = "Create sandbox/status.txt containing ready, then verify it exists"
    result = runtime.run(goal, target_path="sandbox/status.txt", target_content="ready")

    target = ws / "sandbox" / "status.txt"
    exists = target.exists()
    content_ok = False
    if exists:
        content_ok = target.read_text(encoding="utf-8").strip() == "ready"

    success = result.success and exists and content_ok
    needed_recovery = any(
        e.phase == "recover" and "Created missing directory" in e.message
        for e in result.trace
    )

    return {
        "task_id": "task_02_create_nested_file",
        "goal": goal,
        "success": success,
        "trace_length": len(result.trace),
        "details": {
            "file_exists": exists,
            "content_correct": content_ok,
            "needed_recovery": needed_recovery,
        },
    }


if __name__ == "__main__":
    outcome = run_task()
    print(outcome)
