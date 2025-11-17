
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
        return f"Simulation(layout={self.layout}, agents={self.agents})"
    
    def __str__(self) -> str:
        return f"Simulation with {len(self.agents)} agents on layout of size {self.layout.width}x{self.layout.height}"

class SimpleSimulation(SimulationBase):
    
    def step(self):
        # Generate new task if no pending tasks are available
        pending_tasks = [t for t in self.tasks if t.status == Task.STATUS_PENDING]
        if len(pending_tasks) == 0:
            self.tasks.append(random_next(self.layout))

        for agent in self.agents:
             # Assign tasks to agent if doesn't have one
            if agent.task is None:
                # Find first pending task
                for task in self.tasks:
                    if task.status == Task.STATUS_PENDING:
                        agent.task = task
                        agent.task.set_status(Task.STATUS_ASSIGNED)
                        break

            # Move agent
            if agent.task is not None:
                if agent.task.status == Task.STATUS_ASSIGNED: # Move towards task
                    if agent.x < agent.task.x:
                        agent.x += 1
                    elif agent.x > agent.task.x:
                        agent.x -= 1
                    elif agent.y < agent.task.y:
                        agent.y += 1
                    elif agent.y > agent.task.y:
                        agent.y -= 1
                    if agent.x == agent.task.x and agent.y == agent.task.y:
                        agent.task.set_status(Task.STATUS_DELIVERING)
                elif agent.task.status == Task.STATUS_DELIVERING: # Move towards output (0,0)
                    if agent.x > 0:
                        agent.x -= 1
                    elif agent.x < 0:
                        agent.x += 1
                    elif agent.y > 0:
                        agent.y -= 1
                    elif agent.y < 0:
                        agent.y += 1
                    if agent.x == 0 and agent.y == 0:
                        agent.task.set_status(Task.STATUS_COMPLETED)
                        self.tasks.remove(agent.task)  # Remove completed task from the list
                        agent.task = None  # Clear task after completion


class RandomSimulation(SimulationBase):

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

   