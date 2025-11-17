
from models.agent import Agent
from models.layout import Layout
import random


class Simulation:
    def __init__(self, layout: Layout, agents: list[Agent]):
        self.layout = layout
        self.agents = agents

    def random_step(self):
        """Perform a random step for each agent in the simulation"""
        for agent in self.agents:
            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up':
                self.try_move(agent, agent.x, agent.y - 1)
            elif direction == 'down':
                self.try_move(agent, agent.x, agent.y + 1)
            elif direction == 'left':
                self.try_move(agent, agent.x - 1, agent.y)
            elif direction == 'right':
                self.try_move(agent, agent.x + 1, agent.y)

    def try_move(self, agent: Agent, new_x: int, new_y: int) -> bool:
        """Attempt to move an agent to a new position if within bounds"""
        if 0 <= new_x < self.layout.width and 0 <= new_y < self.layout.height:
            agent.x = new_x
            agent.y = new_y
            return True
        return False

    def __repr__(self):
        return f"Simulation(layout={self.layout}, agents={self.agents})"
    
    def __str__(self) -> str:
        return f"Simulation with {len(self.agents)} agents on layout of size {self.layout.width}x{self.layout.height}"