
class Task:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Task(x={self.x}, y={self.y})"
    
    def __str__(self) -> str:
        return f"Task at position ({self.x}, {self.y})"