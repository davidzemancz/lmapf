from dataclasses import dataclass
from models.task import Task
from models.agent import Agent
from models.layout import Layout


@dataclass
class SimulationBase:
    layout: Layout
    agents: list[Agent]
    tasks: list[Task]

    def step(self):
        """Perform a simulation step. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")
