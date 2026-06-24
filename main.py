from PyQt6.QtWidgets import QApplication, QMainWindow,  QStackedWidget
from ui.start_window import StartScreen
from ui.simulation_window import SimulationScreen
import sys


# Main window for simulation containing stacked widget
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clutch Time")
        self.setGeometry(100, 100, 1100, 700)

        # Create Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Adding Screens
        self.simulation_screen = SimulationScreen(self.stacked_widget)
        self.start_screen = StartScreen(self.stacked_widget, self.simulation_screen)
        

        self.stacked_widget.simulation_screen = self.simulation_screen
        self.stacked_widget.addWidget(self.start_screen)  # Index 0 (start)
        self.stacked_widget.addWidget(self.simulation_screen)  # Index 1 (sim)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
