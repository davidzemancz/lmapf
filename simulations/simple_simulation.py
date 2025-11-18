from models.task import Task
from generators.task import random_next
from models.simulation import SimulationBase


class SimpleSimulation(SimulationBase):
    
    def step(self):
        for agent in self.agents:
            # Generate new task if no pending tasks are available
            pending_tasks = [t for t in self.tasks if t.status == Task.STATUS_PENDING]
            if len(pending_tasks) == 0:
                self.tasks.append(random_next(self.layout))

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