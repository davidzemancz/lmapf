
import random
from typing import List
from models.agent import Agent
from models.layout import Layout


def initialize_positions(agents: List[Agent], layout: Layout) -> None:
    """Randomly initialize agent positions on empty cells of the layout"""
    empty_cells = [
        (x, y)
        for y in range(layout.height)
        for x in range(layout.width)
        if layout.get_value(x, y) == Layout.CELL_EMPTY or layout.get_value(x, y) == Layout.CELL_FLOORBOX or layout.get_value(x, y) == Layout.CELL_OUTPUT
    ]
    
    random.shuffle(empty_cells)
    
    for agent in agents:
        if empty_cells:
            agent.x, agent.y = empty_cells.pop()
        else:
            raise ValueError("Not enough empty cells to place all agents")