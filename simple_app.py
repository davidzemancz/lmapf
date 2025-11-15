import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QTextEdit, QPushButton, QLabel
)


class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple PySide6 App")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel with vertical layout
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(200)
        
        # Add label
        label = QLabel("Controls")
        left_layout.addWidget(label)
        
        # Add text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter text here...")
        self.text_input.setMaximumHeight(100)
        left_layout.addWidget(self.text_input)
        
        # Add buttons
        button1 = QPushButton("Button 1")
        button1.clicked.connect(lambda: self.on_button_click("Button 1"))
        left_layout.addWidget(button1)
        
        button2 = QPushButton("Button 2")
        button2.clicked.connect(lambda: self.on_button_click("Button 2"))
        left_layout.addWidget(button2)
        
        button3 = QPushButton("Button 3")
        button3.clicked.connect(lambda: self.on_button_click("Button 3"))
        left_layout.addWidget(button3)
        
        clear_button = QPushButton("Clear Text")
        clear_button.clicked.connect(self.clear_text)
        left_layout.addWidget(clear_button)
        
        # Add stretch to push everything to the top
        left_layout.addStretch()
        
        # Create right panel (placeholder for future content)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_label = QLabel("Main Content Area\n(Your simulation can go here)")
        right_label.setStyleSheet("background-color: #f0f0f0; padding: 20px;")
        right_layout.addWidget(right_label)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
    
    def on_button_click(self, button_name):
        """Handle button clicks"""
        current_text = self.text_input.toPlainText()
        self.text_input.setPlainText(f"{current_text}\n{button_name} clicked!")
    
    def clear_text(self):
        """Clear the text input"""
        self.text_input.clear()


def main():
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
