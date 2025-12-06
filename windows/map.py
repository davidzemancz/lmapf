from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from models.simulation import SimulationBase
from models.layout import Layout


class MapWindow(QMainWindow):
    def __init__(self, simulation: SimulationBase, cell_size: int = 40, tick_interval: int = 500):
        super().__init__()
        self.simulation = simulation
        self.tick_interval = tick_interval
        self.step_count = 0
        
        self.setWindowTitle("Map Layout")
        
        # Create timer for automatic steps
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.setInterval(tick_interval)  # milliseconds
        
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel for buttons
        left_panel = QWidget()
        left_panel.setFixedWidth(150)
        button_layout = QVBoxLayout(left_panel)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Simulation Control section
        sim_control_label = QLabel("Simulation Control")
        sim_control_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        button_layout.addWidget(sim_control_label)
        
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.step_button = QPushButton("Step")
        self.reset_button = QPushButton("Reset")
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.reset_button)
        
        # Add separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        button_layout.addWidget(separator1)
        
        # Speed Control section
        speed_control_label = QLabel("Speed Control")
        speed_control_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        button_layout.addWidget(speed_control_label)
        
        self.speed_up_button = QPushButton("Speed Up")
        self.slow_down_button = QPushButton("Slow Down")
        
        button_layout.addWidget(self.speed_up_button)
        button_layout.addWidget(self.slow_down_button)
        
        # Add separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        button_layout.addWidget(separator2)
        
        # Statistics section
        stats_label = QLabel("Statistics")
        stats_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        button_layout.addWidget(stats_label)
        
        self.steps_label = QLabel(f"Steps: {self.step_count}")
        self.speed_label = QLabel(f"Speed: {self.tick_interval}ms")
        self.tasks_label = QLabel(f"Tasks: 0/{len(simulation.tasks)}")
        
        button_layout.addWidget(self.steps_label)
        button_layout.addWidget(self.speed_label)
        button_layout.addWidget(self.tasks_label)
        
        # Add left panel to main layout
        main_layout.addWidget(left_panel)
        
        # Create canvas for drawing
        self.canvas = MapCanvas(simulation)
        main_layout.addWidget(self.canvas)
        
        # Connect button signals
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        self.step_button.clicked.connect(self.on_step)
        self.reset_button.clicked.connect(self.on_reset)
        self.speed_up_button.clicked.connect(self.on_speed_up)
        self.slow_down_button.clicked.connect(self.on_slow_down)
        
        # Set initial window size based on grid dimensions
        window_width = simulation.layout.width * cell_size + 170  # Extra space for left panel
        window_height = simulation.layout.height * cell_size + 20
        self.resize(window_width, window_height)
    
    def on_timer_tick(self):
        """Called automatically by timer"""
        self.simulation.step()
        self.step_count += 1
        self.update_stats()
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
        self.simulation.step()
        self.step_count += 1
        self.update_stats()
        self.canvas.update()  # Trigger repaint
        print("Step executed")
    
    def on_reset(self):
        """Handle reset button click"""
        self.timer.stop()
        self.step_count = 0
        self.update_stats()
        # Reset agents to initial positions - you can implement this as needed
        print("Reset button clicked")
    
    def on_speed_up(self):
        """Handle speed up button click - decrease interval by 20%"""
        self.tick_interval = max(5, int(self.tick_interval * 0.8))  # Min 5ms
        self.timer.setInterval(self.tick_interval)
        self.update_stats()
        print(f"Speed increased - interval: {self.tick_interval}ms")
    
    def on_slow_down(self):
        """Handle slow down button click - increase interval by 25%"""
        self.tick_interval = min(5000, int(self.tick_interval * 1.25))  # Max 5000ms
        self.timer.setInterval(self.tick_interval)
        self.update_stats()
        print(f"Speed decreased - interval: {self.tick_interval}ms")
    
    def update_stats(self):
        """Update the statistics labels"""
        from models.task import Task
        completed = sum(1 for t in self.simulation.tasks if t.status == Task.STATUS_COMPLETED)
        self.steps_label.setText(f"Steps: {self.step_count}")
        self.speed_label.setText(f"Speed: {self.tick_interval}ms")
        self.tasks_label.setText(f"Tasks: {completed}/{len(self.simulation.tasks)}")


class MapCanvas(QWidget):
    def __init__(self, simulation: SimulationBase):
        super().__init__()
        self.simulation = simulation
        
        # Define colors for different cell types
        self.colors = {
            Layout.CELL_EMPTY: QColor(255, 255, 255),      # White
            Layout.CELL_STORAGE: QColor(100, 150, 255),     # Blue
            Layout.CELL_OUTPUT: QColor(255, 150, 100)       # Orange
        }
        
        # Colors
        self.agent_color = QColor(255, 0, 0)  # Red
        self.task_color = QColor(0, 200, 0)   # Green
    
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
        
        # Draw tasks
        from models.task import Task
        delivery_color = QColor(255, 165, 0)  # Orange for delivery locations
        for task in self.simulation.tasks:
            # Draw pending tasks (pickup location)
            if task.status == Task.STATUS_PENDING:
                task_rect = QRect(
                    int(task.x * cell_size + offset_x),
                    int(task.y * cell_size + offset_y),
                    int(cell_size),
                    int(cell_size)
                )
                painter.fillRect(task_rect, self.task_color)

                # Draw agent ID if task is targeted by an agent
                for agent in self.simulation.agents:
                    if agent.target_task == task:
                        painter.setPen(QPen(QColor(255, 255, 255), 2))
                        font = QFont()
                        font.setPointSize(max(10, int(cell_size / 2.5)))
                        font.setBold(True)
                        painter.setFont(font)
                        painter.drawText(task_rect, Qt.AlignmentFlag.AlignCenter, str(agent.id))
                        break

            # Draw delivering tasks (delivery location)
            if task.status == Task.STATUS_DELIVERING and task.delivery_x is not None:
                delivery_rect = QRect(
                    int(task.delivery_x * cell_size + offset_x),
                    int(task.delivery_y * cell_size + offset_y),
                    int(cell_size),
                    int(cell_size)
                )
                painter.fillRect(delivery_rect, delivery_color)

                # Draw agent ID on delivery location
                for agent in self.simulation.agents:
                    if agent.task == task:
                        painter.setPen(QPen(QColor(255, 255, 255), 2))
                        font = QFont()
                        font.setPointSize(max(10, int(cell_size / 2.5)))
                        font.setBold(True)
                        painter.setFont(font)
                        painter.drawText(delivery_rect, Qt.AlignmentFlag.AlignCenter, str(agent.id))
                        break
        
        # Draw agents as circles
        for agent in self.simulation.agents:
            agent_rect = QRect(
                int(agent.x * cell_size + offset_x),
                int(agent.y * cell_size + offset_y),
                int(cell_size),
                int(cell_size)
            )
            painter.setBrush(self.agent_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(agent_rect)
            
            # Draw agent ID
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            font = QFont()
            font.setPointSize(max(10, int(cell_size / 2.5)))
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(agent_rect, Qt.AlignmentFlag.AlignCenter, str(agent.id))
