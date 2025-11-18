from models.task import Task


class Agent:
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y
        self.task : Task | None = None

    def __repr__(self):
        return f"Agent(id={self.id}, x={self.x}, y={self.y}, task={self.task!r})"
    
    def __str__(self) -> str:
        task_str = f" with task {self.task}" if self.task else " (no task)"
        return f"Agent {self.id} at position ({self.x}, {self.y}){task_str}"
