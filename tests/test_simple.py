import sys
from PySide6.QtWidgets import QApplication
from models.layout import Layout
from models.agent import Agent
from models.task import Task
from simulations.simple_simulation import SimpleSimulation
from windows.map import MapWindow
from generators.layout import storage_floor, storage_walls, obstacle_walls
from generators.agent import initialize_positions
from generators.task import random_next


def test_simple():
    # Create a sample layout
    layout = obstacle_walls(31, 30)

    # Create 5 agents
    agents = [Agent(id=i, x=0, y=0) for i in range(10)]

    # Initialize agent positions
    initialize_positions(agents, layout)

    # Create some initial tasks
    tasks = [random_next(layout) for _ in range(0)]

    # Create simulation
    simulation = SimpleSimulation(layout, agents, tasks)

    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show window
    window = MapWindow(simulation, cell_size=50, tick_interval=500)
    window.show()

    # Run application
    sys.exit(app.exec())

