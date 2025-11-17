from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QPen
from models.layout import Layout


class MapWindow(QMainWindow):
    def __init__(self, map_layout: Layout, cell_size: int = 40):
        super().__init__()
        self.map_layout = map_layout
        
        self.setWindowTitle("Map Layout")
        
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create canvas for drawing
        self.canvas = MapCanvas(map_layout)
        main_layout.addWidget(self.canvas)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Create buttons
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")
        
        # Add buttons to layout
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.reset_button)
        
        # Add button layout to main layout
        main_layout.addLayout(button_layout)
        
        # Connect button signals
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.reset_button.clicked.connect(self.on_reset)
        
        # Set initial window size based on grid dimensions
        window_width = map_layout.width * cell_size + 20
        window_height = map_layout.height * cell_size + 80  # Extra space for buttons
        self.resize(window_width, window_height)
    
    def on_start(self):
        """Handle start button click"""
        print("Start button clicked")
    
    def on_stop(self):
        """Handle stop button click"""
        print("Stop button clicked")
    
    def on_reset(self):
        """Handle reset button click"""
        print("Reset button clicked")


class MapCanvas(QWidget):
    def __init__(self, map_layout: Layout):
        super().__init__()
        self.map_layout = map_layout
        
        # Define colors for different cell types
        self.colors = {
            Layout.CELL_EMPTY: QColor(255, 255, 255),      # White
            Layout.CELL_STORAGE: QColor(100, 150, 255),     # Blue
            Layout.CELL_OUTPUT: QColor(255, 150, 100)       # Orange
        }
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate cell size based on current widget size
        padding = 20
        available_width = self.width() - padding
        available_height = self.height() - padding
        
        cell_width = available_width / self.map_layout.width
        cell_height = available_height / self.map_layout.height
        
        # Use the smaller dimension to keep cells square
        cell_size = min(cell_width, cell_height)
        
        # Calculate offset to center the grid
        offset_x = (self.width() - (cell_size * self.map_layout.width)) / 2
        offset_y = (self.height() - (cell_size * self.map_layout.height)) / 2
        
        # Draw grid
        for y in range(self.map_layout.height):
            for x in range(self.map_layout.width):
                cell_value = self.map_layout.get_value(x, y)
                
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
