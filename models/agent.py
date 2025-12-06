from dataclasses import dataclass, field
from models.task import Task


@dataclass
class Agent:
    id: int
    x: int
    y: int
    task: Task | None = None  # assigned task (delivering)
    target_task: Task | None = None  # target task (heading to pickup)
    goal_x: int = 0  # current goal x (defaults to 0, should be initialized to agent position)
    goal_y: int = 0  # current goal y (defaults to 0, should be initialized to agent position)
    elapsed: int = 0  # timesteps since reaching goal (for priority)
    tie_breaker: float = field(default_factory=lambda: 0.0)  # for priority tie-breaking
