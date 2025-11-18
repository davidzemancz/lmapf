
class Task:
    STATUS_PENDING = 'pending'
    STATUS_ASSIGNED = 'assigned'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.status = Task.STATUS_PENDING

    def set_status(self, status: str):
        self.status = status

    def __repr__(self):
        return f"Task(x={self.x}, y={self.y}, status={self.status!r})"
    
    def __str__(self) -> str:
        return f"Task at position ({self.x}, {self.y}) [status: {self.status}]"