import sys
import random
from PySide6.QtWidgets import QApplication
from generators.task import next_random
from models.layout import Layout
from models.agent import Agent
from models.task import Task
from simulations.pibt_mapd_simulation import PIBTMAPDSimulation
from windows.map import MapWindow
from generators.layout import storage_floor, storage_walls, obstacle_walls
from generators.agent import initialize_positions_randomly

class PIBTMAPDSimulationWithTaskReveal(PIBTMAPDSimulation):
    """Extended PIBT MAPD simulation that reveals tasks over time."""

    def __init__(self, layout: Layout, agents: list[Agent], tasks: list[Task],
                 reveal_interval: int = 10, seed: int = 0):
        super().__init__(layout, agents, tasks, seed)
        self.reveal_interval = reveal_interval
        self.timestep = 0

    def step(self) -> list[tuple[int, int]] | None:
        """Perform one simulation step, revealing tasks at intervals."""
        # Reveal tasks at intervals
        if self.timestep % self.reveal_interval == 0:
            for task in self.tasks:
                if task.status == Task.STATUS_NOTREVEALED:
                    task.status = Task.STATUS_PENDING
                    print(f"Task revealed: pickup=({task.x}, {task.y}) -> delivery=({task.delivery_x}, {task.delivery_y})")
                    break  # Reveal one task per interval

        self.timestep += 1

        # Perform normal PIBT step
        return super().step()


def pibt_mapd_demo():
    # Create a sample layout with storage cells
    layout = storage_walls(30, 30)

    # Create agents
    num_agents = 200
    agents = [Agent(id=i, x=0, y=0) for i in range(num_agents)]

    # Initialize agent positions randomly
    initialize_positions_randomly(agents, layout)

    # Create tasks (initially not revealed)
    num_tasks = 5_000
    tasks = [next_random(layout) for _ in range(num_tasks)]

    # Create simulation with task reveal every 10 timesteps
    simulation = PIBTMAPDSimulationWithTaskReveal(
        layout, agents, tasks,
        reveal_interval=1,
        seed=42
    )

    print(f"Created MAPD simulation with {num_agents} agents and {num_tasks} tasks")
    print("Tasks will be revealed over time...")

    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show window
    window = MapWindow(simulation, cell_size=30, tick_interval=200)
    window.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    pibt_mapd_demo()
