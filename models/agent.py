from dataclasses import dataclass
from models.task import Task


@dataclass
class Agent:
    id: int
    x: int
    y: int
    task: Task | None = None
