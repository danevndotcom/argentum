"""
Argentum Runtime v0.1
Observe → Reason → Plan → Act → Verify → Recover
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import time
import os


@dataclass
class TraceEntry:
    phase: str
    message: str
    success: bool = True
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunResult:
    goal: str
    success: bool
    trace: list[TraceEntry]
    final_state: dict[str, Any] = field(default_factory=dict)


class ArgentumRuntime:
    def __init__(self, workspace: Path | None = None):
        self.workspace = workspace or Path.cwd()
        self.trace: list[TraceEntry] = []

    def _log(self, phase: str, message: str, success: bool = True, **data):
        entry = TraceEntry(phase=phase, message=message, success=success, data=data)
        self.trace.append(entry)
        status = "✓" if success else "✗"
        print(f"[{phase.upper():8}] {status}  {message}")

    # ------------------------------------------------------------------
    # The six phases
    # ------------------------------------------------------------------

    def observe(self, goal: str) -> dict[str, Any]:
        """Look at the current state of the workspace."""
        files = sorted([p.name for p in self.workspace.iterdir() if p.is_file()])
        dirs = sorted([p.name for p in self.workspace.iterdir() if p.is_dir()])

        observation = {
            "cwd": str(self.workspace),
            "files": files,
            "dirs": dirs,
            "goal": goal,
        }
        self._log("observe", f"Workspace has {len(files)} files, {len(dirs)} dirs", data=observation)
        return observation

    def reason(self, observation: dict[str, Any]) -> str:
        """Simple reasoning about what needs to happen."""
        goal = observation["goal"].lower()
        if "ping.txt" in goal or "create a file" in goal:
            thought = "Goal requires creating a file named ping.txt with content 'pong'."
        else:
            thought = f"Goal is: {observation['goal']}. Will attempt a generic file action."
        self._log("reason", thought)
        return thought

    def plan(self, thought: str) -> list[str]:
        """Produce a short list of concrete steps."""
        steps = [
            "Create file ping.txt",
            "Write content 'pong' into it",
            "Verify the file exists and has correct content",
        ]
        self._log("plan", f"{len(steps)} steps planned", steps=steps)
        return steps

    def act(self, steps: list[str]) -> dict[str, Any]:
        """Execute the planned actions on the filesystem."""
        target = self.workspace / "ping.txt"
        try:
            target.write_text("pong\n", encoding="utf-8")
            result = {
                "action": "write_file",
                "path": str(target),
                "content": "pong",
                "success": True,
            }
            self._log("act", f"Created {target.name} with content 'pong'")
            return result
        except Exception as e:
            result = {"action": "write_file", "success": False, "error": str(e)}
            self._log("act", f"Failed to create file: {e}", success=False)
            return result

    def verify(self, action_result: dict[str, Any]) -> bool:
        """Check whether the action actually succeeded."""
        target = self.workspace / "ping.txt"
        exists = target.exists()
        content_ok = False
        if exists:
            content = target.read_text(encoding="utf-8").strip()
            content_ok = content == "pong"

        success = exists and content_ok
        msg = "File exists and content is correct" if success else "Verification failed"
        self._log("verify", msg, success=success, exists=exists, content_ok=content_ok)
        return success

    def recover(self, failed: bool) -> bool:
        """If something failed, try a simple recovery."""
        if not failed:
            self._log("recover", "No recovery needed")
            return True

        self._log("recover", "Attempting recovery: re-create the file")
        target = self.workspace / "ping.txt"
        try:
            target.write_text("pong\n", encoding="utf-8")
            self._log("recover", "Recovery write succeeded")
            return True
        except Exception as e:
            self._log("recover", f"Recovery failed: {e}", success=False)
            return False

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------

    def run(self, goal: str) -> RunResult:
        self.trace = []
        print(f"\n{'='*60}")
        print(f"ARGENTUM  |  Goal: {goal}")
        print(f"{'='*60}\n")

        observation = self.observe(goal)
        thought = self.reason(observation)
        steps = self.plan(thought)
        action_result = self.act(steps)
        verified = self.verify(action_result)

        if not verified:
            recovered = self.recover(failed=True)
            # Re-verify after recovery
            verified = self.verify(action_result) if recovered else False
        else:
            self.recover(failed=False)

        print(f"\n{'='*60}")
        print(f"RESULT: {'SUCCESS' if verified else 'FAILURE'}")
        print(f"{'='*60}\n")

        return RunResult(
            goal=goal,
            success=verified,
            trace=self.trace,
            final_state={"ping.txt_exists": (self.workspace / "ping.txt").exists()},
        )


# ------------------------------------------------------------------
# Simple CLI entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    runtime = ArgentumRuntime()
    result = runtime.run("Create a file named ping.txt containing pong, then verify it exists")
    print(f"Trace entries: {len(result.trace)}")
    print(f"Final success: {result.success}")