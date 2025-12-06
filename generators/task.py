
import random
from models.layout import Layout
from models.task import Task


def next_random(layout: Layout) -> Task:
    """Create a MAPD task with random pickup and delivery locations."""
    # Pick random pickup location from storage cells
    pickup_idx = random.randint(0, len(layout.storage_cells) - 1)
    pickup_x, pickup_y = layout.storage_cells[pickup_idx]

    # Pick random delivery location from output cells
    delivery_idx = random.randint(0, len(layout.output_cells) - 1)
    while delivery_idx == pickup_idx:
        delivery_idx = random.randint(0, len(layout.output_cells) - 1)
    delivery_x, delivery_y = layout.output_cells[delivery_idx]

    return Task(
        x=pickup_x,
        y=pickup_y,
        delivery_x=delivery_x,
        delivery_y=delivery_y,
        status=Task.STATUS_NOTREVEALED,
    )
