class Agent:
    def __init__(self, id: int, x: int, y: int):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Agent(id={self.id}, x={self.x}, y={self.y})"
    
    def __str__(self) -> str:
        return f"Agent {self.id} at position ({self.x}, {self.y})"
