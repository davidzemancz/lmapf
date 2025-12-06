from dataclasses import dataclass, field

import numpy as np

from models.coord import Coord


Grid = np.ndarray  # 2D boolean array, grid[y, x] -> True: traversable, False: obstacle


@dataclass
class Layout:
    CELL_EMPTY = 0
    CELL_STORAGE = 1
    CELL_OBSTACLE = 2
    CELL_OUTPUT = 3

    width: int
    height: int
    cells: list[list[int]] = field(init=False)
    storage_cells: list[Coord] = field(init=False)
    output_cells: list[Coord] = field(init=False)
    _grid_cache: Grid | None = field(init=False, default=None, repr=False)

    def __post_init__(self):
        self.cells = [[Layout.CELL_EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.storage_cells = []
        self.output_cells = []
        self._grid_cache = None

    @staticmethod
    def traversable_cells() -> set[int]:
        return {Layout.CELL_EMPTY, Layout.CELL_OUTPUT, Layout.CELL_STORAGE}

    def set_value(self, x: int, y: int, value: int):
        self.cells[y][x] = value
        self._grid_cache = None  # Invalidate cache

    def get_value(self, x: int, y: int) -> int:
        return self.cells[y][x]

    def is_traversable(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and self.cells[y][x] in Layout.traversable_cells()

    @property
    def grid(self) -> Grid:
        """Get numpy boolean grid representation (cached).

        Returns:
            2D boolean array where grid[y, x] is True if traversable.
        """
        if self._grid_cache is None:
            self._grid_cache = np.zeros((self.height, self.width), dtype=bool)
            traversable = Layout.traversable_cells()
            for y in range(self.height):
                for x in range(self.width):
                    self._grid_cache[y, x] = self.cells[y][x] in traversable
        return self._grid_cache

    def compute_storage_cells(self):
        self.storage_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.get_value(x, y) == Layout.CELL_STORAGE
        ]

    def compute_output_cells(self):
        self.output_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.get_value(x, y) == Layout.CELL_OUTPUT
        ]
