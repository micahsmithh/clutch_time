from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QStackedWidget, QComboBox, QVBoxLayout, QSpinBox
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt  
import sys
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonteamroster

class StartScreen(QWidget):
    def __init__(self, stacked_widget, sim_screen):
        super().__init__()
        self.stacked_widget = stacked_widget  # Reference to switch screens
        self.simulation_screen = sim_screen   #reference simulation screen

        # VARIABLES


        # Grid Layout
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        # Title (Centered Across 3 Columns)
        title = QLabel("🏀 Clutch Time 🏀")
        title.setFont(QFont("Helvetica", 40, QFont.Weight.Bold))
        title.setStyleSheet("color: orange;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(title, 0, 0, 1, 3) # row 0, column 0, spans 1 row, spans 3 rows

        # NBA Logo
        nba_label = QLabel(self)
        nba_pixmap = QPixmap("nba_images/nba_logo.png")  

        # Scale Image
        scaled_nba_pixmap = nba_pixmap.scaled(150, 150, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        nba_label.setPixmap(scaled_nba_pixmap)
        nba_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(nba_label, 1, 1)

        # Start Button (Switch to Simulation Screen)
        start_button = QPushButton("Start Simulation")
        start_button.setFont(QFont("Helvetica", 14))
        start_button.setStyleSheet("background-color: green; color: white; padding: 10px;")
        start_button.clicked.connect(self.start_sim)  #will start simulation
        grid_layout.addWidget(start_button, 3, 0)

        #############################################################
        # TEAM SELECTIONS
        #############################################################

        # Player's Team
        player_team_widget = QWidget()
        player_team_layout = QVBoxLayout()
        player_team_layout.setSpacing(2) 

        self.player_team_label = QLabel(" Select Your Team")
        self.player_team_label.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
        player_team_layout.addWidget(self.player_team_label)

        self.player_team_select = QComboBox()
        self.player_team_select.currentIndexChanged.connect(self.player_team_changed)
        self.player_team_select.setFont(QFont("Helvetica", 14))
        player_team_layout.addWidget(self.player_team_select)

        player_team_widget.setLayout(player_team_layout)
        grid_layout.addWidget(player_team_widget, 2, 0)  #add to main widget

        
        # get full list of teams and show in selection box by team name
        teams_list = teams.get_teams()
        sorted_teams = sorted(teams_list, key = lambda team: team["full_name"])
        for team in sorted_teams:
            self.player_team_select.addItem(team["full_name"])

        # CPU Selection
        cpu_team_widget = QWidget()
        cpu_team_layout = QVBoxLayout()
        cpu_team_layout.setSpacing(1) 

        self.cpu_team_label = QLabel(" Select CPU Team")
        self.cpu_team_label.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
        cpu_team_layout.addWidget(self.cpu_team_label)

        self.cpu_team_select = QComboBox()

        self.cpu_team_select.currentIndexChanged.connect(self.cpu_team_changed)
        self.cpu_team_select.setFont(QFont("Helvetica", 14))
        cpu_team_layout.addWidget(self.cpu_team_select)

        cpu_team_widget.setLayout(cpu_team_layout)
        grid_layout.addWidget(cpu_team_widget, 2, 2)  #add to main widget
        
        # get full list of teams and show in selection box by team name
        for team in sorted_teams:
            self.cpu_team_select.addItem(team["full_name"])

        #############################################################
        # SELECT SCORES
        #############################################################

        # Player Score Selector
        self.player_score_label = QLabel(" Select Your Score")
        self.player_score_label.setFont(QFont("Helvetica", 12))
        player_team_layout.addWidget(self.player_score_label)

        self.player_score_box = QSpinBox()
        self.player_score_box.setFont(QFont("Helvetica", 12))
        self.player_score_box.setRange(0, 150)  #can select from 0 to 150
        self.player_score_box.setValue(0)       #defaults to 0
        player_team_layout.addWidget(self.player_score_box)
        
        # CPU Score Selector
        self.cpu_score_label = QLabel(" Select CPU Score")
        self.cpu_score_label.setFont(QFont("Helvetica", 12))
        cpu_team_layout.addWidget(self.cpu_score_label)

        self.cpu_score_box = QSpinBox()
        self.cpu_score_box.setFont(QFont("Helvetica", 12))
        self.cpu_score_box.setRange(0, 150)
        self.cpu_score_box.setValue(0)
        cpu_team_layout.addWidget(self.cpu_score_box)


        

        #############################################################
        # QUIT BUTTON
        #############################################################

        # Quit Button
        quit_button = QPushButton("Quit")
        quit_button.setFont(QFont("Helvetica", 14))
        quit_button.setStyleSheet("background-color: red; color: white; padding: 10px;")
        quit_button.clicked.connect(lambda: QApplication.quit())
        grid_layout.addWidget(quit_button, 3, 2)

    def start_sim(self):
        # Switch to index 1: SimulationScreen
        self.stacked_widget.setCurrentIndex(1)  

        print(f"Player's Team = {self.simulation_screen.player_team}")
        print(f"CPU's Team = {self.simulation_screen.cpu_team}")

    #selects player team
    def player_team_changed(self):
        selected_team = self.player_team_select.currentText()
        self.simulation_screen.update_player_team(selected_team)

    def cpu_team_changed(self):
        selected_team = self.cpu_team_select.currentText()
        self.simulation_screen.update_cpu_team(selected_team)

#need to edit
class SimulationScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.player_team = None
        self.cpu_team = None

        layout = QGridLayout()
        self.setLayout(layout)

        label = QLabel("🏀 Welcome to the Simulation! 🏀")
        label.setFont(QFont("Helvetica", 30, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, 0, 0, 1, 2)

        # Back Button (Switch back to Start Screen)
        back_button = QPushButton("Back to Main Menu")
        back_button.setFont(QFont("Helvetica", 14))
        back_button.setStyleSheet("background-color: blue; color: white; padding: 10px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, 1, 0, 1, 2)

    #update selected team (called from start)
    def update_player_team(self, player_team):
        self.player_team = teams.find_teams_by_full_name(player_team)

        #gonna have to update text labels
    def update_cpu_team(self, cpu_team):
        self.cpu_team = teams.find_teams_by_full_name(cpu_team)
        #gonna have to update text labels

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basketball Simulation")
        self.setGeometry(100, 100, 900, 600)

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
