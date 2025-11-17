
import random
from models.agent import Agent
from models.layout import Layout


def initialize_positions(agents: List[Agent], layout: Layout) -> None:
    """Initialize agents at random positions within the layout"""
    for agent in agents:
        agent.x = random.randint(0, layout.width - 1)
        agent.y = random.randint(0, layout.height - 1)