"""
Argentum runtime — core control loop.

Implements Observe -> Reason -> Plan -> Act -> Verify -> Recover as a real
orchestrator. observe/act/verify are wired to real filesystem behavior for
the hello-world task (create ping.txt containing "pong"). reason/plan stay
as pass-throughs for now — there's no real decision to make on a fixed,
single-step task. That's the next thing to build once there's more than
one task.

Drop this in as src/runtime/loop.py (overwrite the previous version).
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("argentum.loop")

TARGET_FILE = "ping.txt"
TARGET_CONTENT = "pong"


@dataclass
class TaskState:
    """Everything the loop needs to track across phases for one task."""

    task_id: str
    goal: str
    observation: Optional[str] = None
    plan: Optional[list[str]] = None
    action_result: Optional[Any] = None
    verified: Optional[bool] = None
    attempts: int = 0
    max_attempts: int = 3
    trace: list[dict] = field(default_factory=list)

    def log_phase(self, phase: str, detail: Any) -> None:
        entry = {"phase": phase, "attempt": self.attempts, "detail": detail}
        self.trace.append(entry)
        log.info("[%s] attempt=%d :: %s", phase.upper(), self.attempts, detail)


def observe(state: TaskState) -> TaskState:
    """Check whether the target file currently exists and what it holds."""
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE) as f:
            state.observation = f"{TARGET_FILE} exists, contains: {f.read()!r}"
    else:
        state.observation = f"{TARGET_FILE} does not exist"
    state.log_phase("observe", state.observation)
    return state


def reason(state: TaskState) -> TaskState:
    """Interpret the observation against the goal.

    Fixed single-step task, so there's nothing to decide yet — this becomes
    a real model call once tasks require judgment.
    """
    state.log_phase("reason", f"goal={state.goal!r}")
    return state


def plan(state: TaskState) -> TaskState:
    """Produce the action to take."""
    state.plan = [f"write {TARGET_CONTENT!r} to {TARGET_FILE}"]
    state.log_phase("plan", state.plan)
    return state


def act(state: TaskState) -> TaskState:
    """Execute the plan against the real filesystem."""
    with open(TARGET_FILE, "w") as f:
        f.write(TARGET_CONTENT)
    state.action_result = f"wrote {TARGET_CONTENT!r} to {TARGET_FILE}"
    state.log_phase("act", state.action_result)
    return state


def verify(state: TaskState) -> TaskState:
    """Check the action against ground truth: does the file exist and hold
    exactly the expected content?"""
    if os.path.exists(TARGET_FILE):
        with open(TARGET_FILE) as f:
            content = f.read().strip()
        state.verified = content == TARGET_CONTENT
    else:
        state.verified = False
    state.log_phase("verify", state.verified)
    return state


def recover(state: TaskState) -> TaskState:
    """Decide how to adjust before the next attempt."""
    state.attempts += 1
    state.log_phase("recover", f"retrying, attempt={state.attempts}")
    return state


PHASES: dict[str, Callable[[TaskState], TaskState]] = {
    "observe": observe,
    "reason": reason,
    "plan": plan,
    "act": act,
    "verify": verify,
    "recover": recover,
}


def run_loop(task_id: str, goal: str, max_attempts: int = 3) -> TaskState:
    """Run the full O-R-P-A-V-R loop for a single task until verified or
    max_attempts is exhausted."""
    state = TaskState(task_id=task_id, goal=goal, max_attempts=max_attempts)

    while state.attempts < state.max_attempts:
        state = observe(state)
        state = reason(state)
        state = plan(state)
        state = act(state)
        state = verify(state)

        if state.verified:
            log.info("Task %s VERIFIED on attempt %d", task_id, state.attempts)
            return state

        state = recover(state)

    log.warning("Task %s FAILED after %d attempts", task_id, state.attempts)
    return state


if __name__ == "__main__":
    result = run_loop(task_id="hello-world", goal=f"create {TARGET_FILE} containing {TARGET_CONTENT}")
    print(f"\nFinal state: verified={result.verified}, attempts={result.attempts}")
    print(f"Trace has {len(result.trace)} entries.")
