import sys
from PySide6.QtWidgets import QApplication
from models.layout import Layout
from models.agent import Agent
from models.simulation import RandomSimulation
from windows.map import MapWindow
from generators.layout import storage_floor, storage_walls
from generators.agent import initialize_positions


def main():
    # Create a sample layout
    layout = storage_walls(31, 30)
    
    # Create 5 agents
    agents = [Agent(id=i, x=0, y=0) for i in range(50)]

    # Initialize agent positions
    initialize_positions(agents, layout)
    
    # Create simulation
    simulation = RandomSimulation(layout, agents)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show window
    window = MapWindow(simulation, cell_size=50, tick_interval=500)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
