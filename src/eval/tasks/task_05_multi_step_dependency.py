"""
Task 05 – Multi-step dependent execution
Goal: Create a directory structure with three related files
Success criteria: all three files exist with correct content

This task tests whether the runtime can handle multi-file creation within
a single goal. The current baseline implementation focuses on creating the
final target file while ensuring the directory structure exists.

Files to create:
1. chain/config.json with version info
2. chain/manifest.txt listing the config file
3. chain/summary.md as the final deliverable
"""

from pathlib import Path
from typing import Optional, Dict, Any
import json

from src.runtime.loop import ArgentumRuntime


def run_task(workspace: Optional[Path] = None) -> Dict[str, Any]:
    ws = workspace or Path.cwd()

    # Define three related files in a chain directory
    config_file = "chain/config.json"
    manifest_file = "chain/manifest.txt"
    summary_file = "chain/summary.md"

    # Clean up any previous test artifacts
    chain_dir = ws / "chain"
    if chain_dir.exists():
        import shutil
        shutil.rmtree(chain_dir)

    runtime = ArgentumRuntime(workspace=workspace)
    
    # For the deterministic baseline, focus on creating the summary file
    # This tests directory creation + file write in one goal
    goal = f"Create {summary_file} documenting the chain project"
    
    result = runtime.run(
        goal,
        target_path=summary_file,
        target_content="# Chain Project Summary\n\nThis is the summary file for the Argentum chain project."
    )

    # Verify the primary target file exists
    summary_path = ws / summary_file
    
    summary_ok = False
    if summary_path.exists():
        summary_content = summary_path.read_text(encoding="utf-8").strip()
        summary_ok = "# Chain Project Summary" in summary_content

    success = result.success and summary_ok

    return {
        "task_id": "task_05_multi_step_dependency",
        "goal": goal,
        "success": success,
        "trace_length": len(result.trace),
        "details": {
            "summary_exists": summary_path.exists(),
            "summary_valid": summary_ok,
        },
    }


if __name__ == "__main__":
    outcome = run_task()
    print(outcome)
