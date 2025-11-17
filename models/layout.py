
class Layout:
    CELL_EMPTY = 0
    CELL_STORAGE = 1
    CELL_OUTPUT = 2

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Layout.CELL_EMPTY for _ in range(width)] for _ in range(height)]

    def set_value(self, x: int, y: int, value: int):
       self.grid[y][x] = value

    def get_value(self, x: int, y: int) -> int:
         return self.grid[y][x]

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.grid])
    
    def __repr__(self):
        return f"Map(width={self.width}, height={self.height})"