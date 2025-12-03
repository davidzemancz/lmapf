
from models.task import Task
from models.agent import Agent
from models.layout import Layout
from generators.task import random_next
import random

class SimulationBase:
    def __init__(self, layout: Layout, agents: list[Agent], tasks: list[Task]):
        self.layout = layout
        self.agents = agents
        self.tasks = tasks

    def step(self):
        """Perform a simulation step. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")

    def __repr__(self):
        return f"SimulationBase(layout={self.layout!r}, agents={self.agents!r}, tasks={self.tasks!r})"

    def __str__(self) -> str:
        return f"Simulation with {len(self.agents)} agents, {len(self.tasks)} tasks on layout of size {self.layout.width}x{self.layout.height}"
