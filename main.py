import sys
from PySide6.QtWidgets import QApplication
from models.layout import Layout
from windows.map import MapWindow
from generators.layout import full_storage


def main():
    # Create a sample layout
    layout = full_storage(11, 10)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show window
    window = MapWindow(layout, cell_size=50)
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
