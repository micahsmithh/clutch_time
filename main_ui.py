from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QStackedWidget, QComboBox, QVBoxLayout, QSpinBox, QMessageBox
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtCore import Qt  
import sys
from nba_api.stats.endpoints import playercareerstats, teamgamelog, boxscoretraditionalv2
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd

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
        # fetch team id
        player_team_id = self.simulation_screen.player_team[0]['id']

        # Open lineup selection window
        self.lineup_window = LineupSelectionWindow(player_team_id, self.lineup_set)
        self.lineup_window.show()


        print(f"Player's Team = {self.simulation_screen.player_team}")
        print(f"CPU's Team = {self.simulation_screen.cpu_team}")
        print(f"Player's Score = {self.player_score_box.value()}")
        print(f"CPU's Score = {self.cpu_score_box.value()}")
    
    def lineup_set(self, selected_players):
        print("Selected Players: ", selected_players)

        self.simulation_screen.set_player_lineup(selected_players)

        # Switch to index 1: SimulationScreen
        self.stacked_widget.setCurrentIndex(1)  


    #selects player team
    def player_team_changed(self):
        selected_team = self.player_team_select.currentText()
        self.simulation_screen.update_player_team(selected_team)

    def cpu_team_changed(self):
        selected_team = self.cpu_team_select.currentText()
        self.simulation_screen.update_cpu_team(selected_team)

class LineupSelectionWindow(QWidget):
    def __init__(self, team_id, callback_function):
        super().__init__()

        #intialize variables
        self.team_id = team_id
        self.callback = callback_function
        self.setWindowTitle("Select Your Lineup")

        self.layout = QGridLayout()
        self.dropdowns = []

        #add widgets for position names
        self.set_label("SF", 0)
        self.set_label("PF", 1)
        self.set_label("C", 2)
        self.set_label("SG", 3)
        self.set_label("PG", 4)

        # Get team roster
        roster = commonteamroster.CommonTeamRoster(team_id=team_id)
        df = roster.get_data_frames()[0]
        self.player_names = list(df['PLAYER'])

        #need to get starting lineup for team
        starters = self.get_starters()

        # 5 dropdown menus for 5 players on the floor and
        for i in range(5):
            dropdown = QComboBox()
            dropdown.addItems(self.player_names)

            # set default from last game's starting lineup
            dropdown.setCurrentText(starters[i])

            self.dropdowns.append(dropdown)         #grabs dropdown value to list
            self.layout.addWidget(dropdown, i, 1)
        


        confirm_button = QPushButton("Confirm Lineup")
        confirm_button.clicked.connect(self.confirm_lineup)
        self.layout.addWidget(confirm_button, 5,  1)

        self.setLayout(self.layout)

    def set_label(self, text, row):
        label = QLabel(text)
        label.setFont(QFont("Helvetica", 10, QFont.Weight.Bold))
        label.setStyleSheet("color: orange;")
        self.layout.addWidget(label, row, 0)
        

    def confirm_lineup(self):
        selected_players = [dropdown.currentText() for dropdown in self.dropdowns]

        if len(set(selected_players)) < 5:
            QMessageBox.warning(self, "Error", "You selected duplicate players!")
            return

        self.callback(selected_players)  # Send selected players back to main app
        self.close() #close window

    def get_starters(self):
        season = '2024' 
        team = next((team['abbreviation'] for team in teams.get_teams() if team['id'] == self.team_id), None) # get abbreivation from team_id

        # Fetch the regular season game log
        gamelog_regular = teamgamelog.TeamGameLog(team_id=self.team_id, season=season, season_type_all_star='Regular Season')
        games_regular = gamelog_regular.get_data_frames()[0]

        # Fetch the playoff game log
        gamelog_playoffs = teamgamelog.TeamGameLog(team_id=self.team_id, season=season, season_type_all_star='Playoffs')
        games_playoffs = gamelog_playoffs.get_data_frames()[0]

        # Combine both regular season and playoff games
        games_combined = pd.concat([games_regular, games_playoffs], ignore_index=True)

        # Sort the combined games by GAME_DATE to get the most recent game
        games_combined['GAME_DATE'] = pd.to_datetime(games_combined['GAME_DATE'])  # Convert GAME_DATE to datetime format
        games_combined_sorted = games_combined.sort_values(by='GAME_DATE', ascending=False)

        # Get the last game (most recent one)
        if not games_combined_sorted.empty:
            for _, game in games_combined_sorted.iterrows():
                game_id = game['Game_ID']
                print(f"Checking Game ID: {game_id}")
                
                # Fetch the box score for the current game
                boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)

                # Get player stats DataFrame
                player_stats = boxscore.get_data_frames()[0]

                #filter players to be only starters from selected team
                team_starters = player_stats[
                    (player_stats['TEAM_ABBREVIATION'] == team) &
                    (player_stats['START_POSITION'].isin(['G', 'F', 'C']))
                ]

                # once team starters are found: display
                if not team_starters.empty:
                    print(f"Found starters for Game ID: {game_id}")
                    print(f"Game details:\n{game}")
                    print(f"Game ID = {game_id}")
                    print(team_starters[['PLAYER_NAME', 'START_POSITION']])
                    return team_starters['PLAYER_NAME'].tolist()  # exit loops when starters are found
            else:
                print(f"No valid starters found in the recent games for {team}.")
                return
        else:
            print(f"No games found for {team}.")
            return

    



#need to edit
class SimulationScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        #setting background screen
        self.background_pixmap = QPixmap("nba_images/basketball_court.jpg")


        self.stacked_widget = stacked_widget

        self.player_team = None
        self.cpu_team = None

        self.player_lineup = []
        self.cpu_lineup = []

        layout = QGridLayout()
        self.setLayout(layout)


        label = QLabel("🏀 Simulation Screen 🏀")
        label.setFont(QFont("Helvetica", 30, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label, 0, 0, 1, 2)

        # Back Button (Switch back to Start Screen)
        back_button = QPushButton("Back to Main Menu")
        back_button.setFont(QFont("Helvetica", 14))
        back_button.setStyleSheet("background-color: blue; color: white; padding: 10px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, 1, 0, 1, 2)

    #update selected teams (called from start) and sets variable to dictionary
    def update_player_team(self, player_team):
        self.player_team = teams.find_teams_by_full_name(player_team)

        #gonna have to update text labels
    def update_cpu_team(self, cpu_team):
        self.cpu_team = teams.find_teams_by_full_name(cpu_team)
        #gonna have to update text labels

        #print(f"Abbreviation: {self.cpu_team[0]['abbreviation']}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    def set_player_lineup(self, player_lineup):
        self.player_lineup = player_lineup

        print(f"Player's Lineup: {self.player_lineup}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basketball Simulation")
        self.setGeometry(100, 100, 900, 500)

        # Create Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Adding Screens
        self.simulation_screen = SimulationScreen(self.stacked_widget)
        self.start_screen = StartScreen(self.stacked_widget, self.simulation_screen)
        

        self.stacked_widget.simulation_screen = self.simulation_screen
        self.stacked_widget.addWidget(self.start_screen)  # Index 0 (start)
        self.stacked_widget.addWidget(self.simulation_screen)  # Index 1 (sim)


def get_team_id_from_abbreviation(abbreviation):
        # Fetch the list of all NBA teams
        all_teams = teams.get_teams()
        
        # Search for the team with the given abbreviation
        for team in all_teams:
            if team['abbreviation'] == abbreviation:
                return team['id']
        
        # If no match is found, return None
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
