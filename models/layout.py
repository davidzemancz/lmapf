
class Layout:
    CELL_EMPTY = 0
    CELL_STORAGE = 1
    CELL_FLOORBOX = 2
    CELL_OBSTACLE = 3
    CELL_OUTPUT = 4

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Layout.CELL_EMPTY for _ in range(width)] for _ in range(height)]

    def set_value(self, x: int, y: int, value: int):
       self.grid[y][x] = value

    def get_value(self, x: int, y: int) -> int:
         return self.grid[y][x]
    
    def is_traversable(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] != Layout.CELL_STORAGE and self.grid[y][x] != Layout.CELL_OBSTACLE

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.grid])
    
    def __repr__(self):
        return f"Map(width={self.width}, height={self.height})"