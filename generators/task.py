
from models.task import Task
from models.layout import Layout
import random

def random_next(layout: Layout) -> Task:
    i = random.randint(0, len(layout.storage_cells) - 1)
    task = Task(layout.storage_cells[i][0], layout.storage_cells[i][1])
    return task