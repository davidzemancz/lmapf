
from models.agent import Agent
from models.layout import Layout
import random

class SimulationBase:
    def __init__(self, layout: Layout, agents: list[Agent]):
        self.layout = layout
        self.agents = agents

    def step(self):
        """Perform a simulation step. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")
    
    def __repr__(self):
        return f"Simulation(layout={self.layout}, agents={self.agents})"
    
    def __str__(self) -> str:
        return f"Simulation with {len(self.agents)} agents on layout of size {self.layout.width}x{self.layout.height}"

class RandomSimulation(SimulationBase):
    def __init__(self, layout: Layout, agents: list[Agent]):
        self.layout = layout
        self.agents = agents

    def step(self):
        """Perform a random step for each agent in the simulation"""
        for agent in self.agents:
            moved = False
            while not moved:
                direction = random.choice(['up', 'down', 'left', 'right'])
                if direction == 'up':
                    moved = self.try_move(agent, agent.x, agent.y - 1)
                elif direction == 'down':
                    moved = self.try_move(agent, agent.x, agent.y + 1)
                elif direction == 'left':
                    moved = self.try_move(agent, agent.x - 1, agent.y)
                elif direction == 'right':
                    moved = self.try_move(agent, agent.x + 1, agent.y)

    def try_move(self, agent: Agent, new_x: int, new_y: int) -> bool:
        """Attempt to move an agent to a new position if within bounds"""
        if self.layout.is_traversable(new_x, new_y) and not any(other_agent.x == new_x and other_agent.y == new_y for other_agent in self.agents if other_agent != agent):
            agent.x = new_x
            agent.y = new_y
            return True
        return False

   