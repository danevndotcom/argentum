"""
Task 04 – Deliberate failure and recovery
Goal: Create a file in a nested directory that does not exist yet
Success criteria: file exists in nested path with correct content

This task tests whether the runtime correctly handles an initial failure
(missing parent directory) and uses the recover() phase to fix the
environment before succeeding. The first write attempt will fail because
the parent directory does not exist; recovery should create the directory
and retry the write.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from src.runtime.loop import ArgentumRuntime


def run_task(workspace: Optional[Path] = None) -> Dict[str, Any]:
    ws = workspace or Path.cwd()

    # Define a nested path where parent directories do NOT exist yet
    nested_rel_path = "nested/deep/config.txt"
    
    # Ensure the nested directory does NOT exist before running
    # This sets up the condition for initial failure
    nested_dir = ws / "nested" / "deep"
    if nested_dir.exists():
        # Clean up any previous test artifacts
        import shutil
        shutil.rmtree(ws / "nested")
    
    target_file = ws / nested_rel_path
    
    runtime = ArgentumRuntime(workspace=workspace)
    goal = f"Create {nested_rel_path} containing 'configured'"
    result = runtime.run(
        goal, 
        target_path=nested_rel_path, 
        target_content="configured"
    )

    exists = target_file.exists()
    content_ok = False
    if exists:
        content_ok = target_file.read_text(encoding="utf-8").strip() == "configured"

    success = result.success and exists and content_ok
    
    # Check if recovery was triggered by examining trace
    recovery_triggered = any(entry.phase == "recover" and entry.message != "No recovery needed" 
                            for entry in result.trace)

    return {
        "task_id": "task_04_deliberate_failure_recovery",
        "goal": goal,
        "success": success,
        "trace_length": len(result.trace),
        "recovery_triggered": recovery_triggered,
        "details": {
            "file_exists": exists,
            "content_correct": content_ok,
            "recovery_used": recovery_triggered,
        },
    }


if __name__ == "__main__":
    outcome = run_task()
    print(outcome)
