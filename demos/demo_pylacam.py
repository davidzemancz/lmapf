import sys
from PySide6.QtWidgets import QApplication
from models.layout import Layout
from models.agent import Agent
from models.task import Task
from simulations.lacam_simulation import PylacamSimulation
from windows.map import MapWindow
from generators.layout import storage_floor, storage_walls, obstacle_walls
from generators.agent import initialize_positions_randomly
from generators.task import random_next


def demo_pylacam():
    # Create a sample layout
    layout = storage_floor(10, 10)

    # Create agents
    agents = [Agent(id=i, x=0, y=0) for i in range(5)]

    # Initialize agent positions
    initialize_positions_randomly(agents, layout)

    # Create tasks and assign to agents
    tasks = []
    for agent in agents:
        task = random_next(layout)
        task.set_status(Task.STATUS_ASSIGNED)
        agent.task = task
        tasks.append(task)

    # Create simulation
    simulation = PylacamSimulation(layout, agents, tasks)

    # Solve the MAPF instance
    print("Solving MAPF instance...")
    solved = simulation.solve(time_limit_ms=5000, verbose=1)
    if solved:
        print(f"Solution found with {len(simulation.solution)} steps")
    else:
        print("No solution found!")
        return

    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show window
    window = MapWindow(simulation, cell_size=50, tick_interval=500)
    window.show()

    # Run application
    sys.exit(app.exec())

