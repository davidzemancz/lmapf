class Agent:
    def __init__(self, id: int, capacity: int, x: int, y: int):
        self.id = id
        self.capacity = capacity
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Agent(id={self.id}, capacity={self.capacity}, x={self.x}, y={self.y})"
