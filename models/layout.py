from dataclasses import dataclass, field


@dataclass
class Layout:
    CELL_EMPTY = 0
    CELL_STORAGE = 1
    CELL_OBSTACLE = 2
    CELL_OUTPUT = 3

    width: int
    height: int
    grid: list[list[int]] = field(init=False)
    storage_cells: list[tuple[int, int]] = field(init=False)

    def __post_init__(self):
        self.grid = [[Layout.CELL_EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.storage_cells = []

    @staticmethod
    def traversable_cells() -> set[int]:
        return {Layout.CELL_EMPTY, Layout.CELL_OUTPUT, Layout.CELL_STORAGE}

    def set_value(self, x: int, y: int, value: int):
        self.grid[y][x] = value

    def get_value(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def is_traversable(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] in Layout.traversable_cells()

    def compute_storage_cells(self):
        self.storage_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.get_value(x, y) == Layout.CELL_STORAGE
        ]
