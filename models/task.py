from dataclasses import dataclass, field


@dataclass
class Task:
    STATUS_NOTREVEALED = 'not_revealed'
    STATUS_PENDING = 'pending'
    STATUS_ASSIGNED = 'assigned'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'

    x: int  # pickup location x
    y: int  # pickup location y
    delivery_x: int | None = None  # delivery location x (optional for MAPF-only tasks)
    delivery_y: int | None = None  # delivery location y (optional for MAPF-only tasks)
    status: str = field(default=STATUS_PENDING)