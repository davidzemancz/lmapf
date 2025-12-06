from dataclasses import dataclass, field

from models.coord import Coord


@dataclass
class Config:
    positions: list[Coord] = field(default_factory=list)

    def __getitem__(self, k: int) -> Coord:
        return self.positions[k]

    def __setitem__(self, k: int, coord: Coord) -> None:
        self.positions[k] = coord

    def __len__(self) -> int:
        return len(self.positions)

    def __iter__(self):
        return iter(self.positions)

    def append(self, coord: Coord) -> None:
        self.positions.append(coord)
