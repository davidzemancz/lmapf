import sys
from PySide6.QtWidgets import QApplication
from models.layout import Layout
from models.agent import Agent
from models.simulation import Simulation
from windows.map import MapWindow
from generators.layout import full_storage


def main():
    # Create a sample layout
    layout = full_storage(11, 10)
    
    # Create one agent
    agent = Agent(id=1, x=5, y=5)
    
    # Create simulation
    simulation = Simulation(layout, [agent])
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show window
    window = MapWindow(simulation, cell_size=50, tick_interval=500)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
