"""
Argentum Agent Loop
Observe → Reason → Plan → Act → Verify → Recover
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class StepStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


@dataclass
class StepResult:
    status: StepStatus
    observation: str
    action_taken: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentState:
    goal: str
    history: List[StepResult] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    step_count: int = 0
    max_steps: int = 20


class ArgentumAgent:
    """Minimal agentic loop skeleton."""

    def __init__(self, goal: str, max_steps: int = 20):
        self.state = AgentState(goal=goal, max_steps=max_steps)

    def observe(self) -> str:
        return f"Observing environment for goal: {self.state.goal}"

    def reason(self, observation: str) -> str:
        return f"Reasoning about: {observation}"

    def plan(self, reasoning: str) -> str:
        return "plan: placeholder_action"

    def act(self, plan: str) -> StepResult:
        return StepResult(
            status=StepStatus.SUCCESS,
            observation="Action executed (placeholder)",
            action_taken=plan,
        )

    def verify(self, result: StepResult) -> bool:
        return result.status == StepStatus.SUCCESS

    def recover(self, result: StepResult) -> None:
        print(f"[Recover] Step failed: {result.error or result.observation}")

    def run(self) -> AgentState:
        print(f"\n=== Argentum Agent started ===")
        print(f"Goal: {self.state.goal}\n")

        while self.state.step_count < self.state.max_steps:
            self.state.step_count += 1
            print(f"--- Step {self.state.step_count} ---")

            observation = self.observe()
            print(f"Observe: {observation}")

            reasoning = self.reason(observation)
            print(f"Reason:  {reasoning}")

            plan = self.plan(reasoning)
            print(f"Plan:    {plan}")

            result = self.act(plan)
            print(f"Act:     {result.action_taken} → {result.status.value}")

            success = self.verify(result)
            self.state.history.append(result)

            if success:
                print("Verify:  SUCCESS")
                break
            else:
                print("Verify:  FAILURE")
                self.recover(result)

        print("\n=== Agent finished ===")
        return self.state


if __name__ == "__main__":
    agent = ArgentumAgent(goal="Demonstrate the Argentum agent loop")
    final_state = agent.run()
    print(f"\nTotal steps: {final_state.step_count}")
