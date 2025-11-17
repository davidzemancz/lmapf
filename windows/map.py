from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QColor, QPen
from models.simulation import Simulation
from models.layout import Layout


class MapWindow(QMainWindow):
    def __init__(self, simulation: Simulation, cell_size: int = 40, tick_interval: int = 500):
        super().__init__()
        self.simulation = simulation
        
        self.setWindowTitle("Map Layout")
        
        # Create timer for automatic steps
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.setInterval(tick_interval)  # milliseconds
        
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create canvas for drawing
        self.canvas = MapCanvas(simulation)
        main_layout.addWidget(self.canvas)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Create buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.step_button = QPushButton("Step")
        self.reset_button = QPushButton("Reset")
        
        # Add buttons to layout
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.reset_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Connect button signals
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.step_button.clicked.connect(self.on_step)
        self.reset_button.clicked.connect(self.on_reset)
        
        # Set initial window size based on grid dimensions
        window_width = simulation.layout.width * cell_size + 20
        window_height = simulation.layout.height * cell_size + 80  # Extra space for buttons
        self.resize(window_width, window_height)
    
    def on_timer_tick(self):
        """Called automatically by timer"""
        self.simulation.random_step()
        self.canvas.update()  # Trigger repaint
    
    def on_start(self):
        """Handle start button click"""
        self.timer.start()
        print("Simulation started")
    
    def on_stop(self):
        """Handle stop button click"""
        self.timer.stop()
        print("Simulation stopped")
    
    def on_step(self):
        """Handle step button click - perform one step"""
        self.simulation.random_step()
        self.canvas.update()  # Trigger repaint
        print("Step executed")
    
    def on_reset(self):
        """Handle reset button click"""
        self.timer.stop()
        # Reset agents to initial positions - you can implement this as needed
        print("Reset button clicked")


class MapCanvas(QWidget):
    def __init__(self, simulation: Simulation):
        super().__init__()
        self.simulation = simulation
        
        # Define colors for different cell types
        self.colors = {
            Layout.CELL_EMPTY: QColor(255, 255, 255),      # White
            Layout.CELL_STORAGE: QColor(100, 150, 255),     # Blue
            Layout.CELL_OUTPUT: QColor(255, 150, 100)       # Orange
        }
        
        # Color for agents
        self.agent_color = QColor(255, 0, 0)  # Red
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate cell size based on current widget size
        padding = 20
        available_width = self.width() - padding
        available_height = self.height() - padding
        
        cell_width = available_width / self.simulation.layout.width
        cell_height = available_height / self.simulation.layout.height
        
        # Use the smaller dimension to keep cells square
        cell_size = min(cell_width, cell_height)
        
        # Calculate offset to center the grid
        offset_x = (self.width() - (cell_size * self.simulation.layout.width)) / 2
        offset_y = (self.height() - (cell_size * self.simulation.layout.height)) / 2
        
        # Draw grid
        for y in range(self.simulation.layout.height):
            for x in range(self.simulation.layout.width):
                cell_value = self.simulation.layout.get_value(x, y)
                
                # Get cell color
                color = self.colors.get(cell_value, QColor(200, 200, 200))
                
                # Calculate cell position
                rect = QRect(
                    int(x * cell_size + offset_x),
                    int(y * cell_size + offset_y),
                    int(cell_size),
                    int(cell_size)
                )
                
                # Fill cell
                painter.fillRect(rect, color)
                
                # Draw cell border
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawRect(rect)
        
        # Draw agents
        for agent in self.simulation.agents:
            agent_rect = QRect(
                int(agent.x * cell_size + offset_x),
                int(agent.y * cell_size + offset_y),
                int(cell_size),
                int(cell_size)
            )
            painter.fillRect(agent_rect, self.agent_color)
