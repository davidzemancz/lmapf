from dataclasses import dataclass, field


@dataclass
class Task:
    STATUS_PENDING = 'pending'
    STATUS_ASSIGNED = 'assigned'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'

    x: int
    y: int
    status: str = field(default=STATUS_PENDING)