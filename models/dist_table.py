from collections import deque
from dataclasses import dataclass, field

import numpy as np

from models.coord import Coord
from models.layout import Grid


def get_neighbors(grid: Grid, coord: Coord) -> list[Coord]:
    """Get valid neighboring coordinates (4-connected grid).

    Args:
        grid: 2D boolean array representing the map.
        coord: Center position (x, y).

    Returns:
        List of valid neighboring coordinates in 4 directions.
    """
    x, y = coord
    neighbors = []

    if x > 0 and grid[y, x - 1]:
        neighbors.append((x - 1, y))
    if x < grid.shape[1] - 1 and grid[y, x + 1]:
        neighbors.append((x + 1, y))
    if y > 0 and grid[y - 1, x]:
        neighbors.append((x, y - 1))
    if y < grid.shape[0] - 1 and grid[y + 1, x]:
        neighbors.append((x, y + 1))

    return neighbors


def is_valid_coord(grid: Grid, coord: Coord) -> bool:
    """Check if a coordinate is valid and free on the grid.

    Args:
        grid: 2D boolean array representing the map.
        coord: Position (x, y) to check.

    Returns:
        True if coordinate is within bounds and not an obstacle.
    """
    x, y = coord
    if x < 0 or x >= grid.shape[1] or y < 0 or y >= grid.shape[0] or not grid[y, x]:
        return False
    return True


@dataclass
class DistTable:
    """Distance table for computing shortest path distances using BFS.

    Uses lazy BFS evaluation - distances are computed on demand and cached.
    Coordinates are in (x, y) format.
    """
    grid: Grid
    goal: Coord  # (x, y)
    _queue: deque[Coord] = field(init=False)
    _table: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        """Initialize distance table with goal position."""
        self._queue = deque([self.goal])
        self._table = np.full(self.grid.shape, self.grid.size, dtype=int)
        gx, gy = self.goal
        self._table[gy, gx] = 0

    def get(self, target: Coord) -> int:
        """Get shortest path distance from target to goal.

        Args:
            target: Target position (x, y).

        Returns:
            Shortest path distance. Returns grid.size if unreachable.
        """
        if not is_valid_coord(self.grid, target):
            return self.grid.size

        tx, ty = target
        # Distance already known
        if int(self._table[ty, tx]) < self._table.size:
            return int(self._table[ty, tx])

        # BFS with lazy evaluation
        while len(self._queue) > 0:
            ux, uy = self._queue.popleft()
            d = int(self._table[uy, ux])
            for vx, vy in get_neighbors(self.grid, (ux, uy)):
                if d + 1 < self._table[vy, vx]:
                    self._table[vy, vx] = d + 1
                    self._queue.append((vx, vy))
            if (ux, uy) == target:
                return d

        return self.grid.size
