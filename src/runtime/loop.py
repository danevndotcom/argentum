"""
Argentum runtime — core control loop.

Implements Observe -> Reason -> Plan -> Act -> Verify -> Recover as a real
orchestrator. Each phase is a typed function with a single responsibility.
This file intentionally contains no model-specific logic; that belongs in
src/model, called from inside reason()/plan() once a client is wired in.

Drop this in as src/runtime/loop.py.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("argentum.loop")


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
    """Gather current environment state relevant to the goal.

    v0.1 stub — replace with real filesystem / git status inspection.
    """
    state.observation = "TODO: real observation of repo state"
    state.log_phase("observe", state.observation)
    return state


def reason(state: TaskState) -> TaskState:
    """Interpret the observation against the goal. Model call goes here."""
    state.log_phase("reason", f"goal={state.goal!r}")
    return state


def plan(state: TaskState) -> TaskState:
    """Produce an ordered list of concrete actions."""
    state.plan = ["TODO: real plan step"]
    state.log_phase("plan", state.plan)
    return state


def act(state: TaskState) -> TaskState:
    """Execute the plan's next action against the real environment."""
    state.action_result = "TODO: real action execution"
    state.log_phase("act", state.action_result)
    return state


def verify(state: TaskState) -> TaskState:
    """Check the action against ground truth (e.g. did tests pass)."""
    state.verified = False  # TODO: real verification
    state.log_phase("verify", state.verified)
    return state


def recover(state: TaskState) -> TaskState:
    """Decide how to adjust the plan before the next attempt."""
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
    # Hello-world smoke test: proves the loop executes end to end and
    # produces a trace, before any real logic is wired in.
    result = run_loop(task_id="hello-world", goal="create ping.txt containing pong")
    print(f"\nFinal state: verified={result.verified}, attempts={result.attempts}")
    print(f"Trace has {len(result.trace)} entries.")
