"""
Task 01 – Create ping.txt
Goal: Create a file named ping.txt containing exactly "pong"
Success criteria: file exists and content == "pong"
"""

from pathlib import Path
from typing import Optional, Dict, Any
from src.runtime.loop import ArgentumRuntime


def run_task(workspace: Optional[Path] = None) -> Dict[str, Any]:
    runtime = ArgentumRuntime(workspace=workspace)
    goal = "Create a file named ping.txt containing pong, then verify it exists"
    result = runtime.run(goal)

    target = (workspace or Path.cwd()) / "ping.txt"
    exists = target.exists()
    content_ok = False
    if exists:
        content_ok = target.read_text(encoding="utf-8").strip() == "pong"

    success = result.success and exists and content_ok

    return {
        "task_id": "task_01_create_ping",
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
