from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QMessageBox,QVBoxLayout, QSpinBox, QCheckBox
from PyQt6.QtGui import QFont, QPixmap
from nba_api.stats.endpoints import commonteamroster, teamgamelog
from nba_api.stats.static import teams
import pandas as pd
from PyQt6.QtCore import Qt
from utilities import request_data  





class StartScreen(QWidget):
    def __init__(self, stacked_widget, sim_screen):
        super().__init__()
        self.stacked_widget = stacked_widget  # Reference to switch screens
        self.simulation_screen = sim_screen   #reference simulation screen



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
        scaled_nba_pixmap = nba_pixmap.scaled(
            150, 150,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
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
        self.player_score_label.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        player_team_layout.addWidget(self.player_score_label)

        self.player_score_box = QSpinBox()
        self.player_score_box.setFont(QFont("Helvetica", 12))
        self.player_score_box.setRange(0, 150)  #can select from 0 to 150
        self.player_score_box.setValue(0)       #defaults to 0
        player_team_layout.addWidget(self.player_score_box)
        
        # CPU Score Selector
        self.cpu_score_label = QLabel(" Select CPU Score")
        self.cpu_score_label.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        cpu_team_layout.addWidget(self.cpu_score_label)

        self.cpu_score_box = QSpinBox()
        self.cpu_score_box.setFont(QFont("Helvetica", 12))
        self.cpu_score_box.setRange(0, 150)
        self.cpu_score_box.setValue(0)
        cpu_team_layout.addWidget(self.cpu_score_box)


        #############################################################
        # Possession Selection
        #############################################################

        self.arrow_left = "←"
        self.arrow_right = "→"
        self.current_direction = "left"

        arrow_layout = QVBoxLayout()
        arrow_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow_widget = QWidget()
        arrow_widget.setLayout(arrow_layout)

        # Possession Label
        self.possession_label = QLabel("Possession")
        self.possession_label.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
        self.possession_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Arrow Button
        self.arrow_button = QPushButton(self.arrow_left)
        self.arrow_button.setFont(QFont("Helvetica", 24))
        self.arrow_button.setFixedSize(50, 50)
        self.arrow_button.clicked.connect(self.toggle_arrow)

        # Add label and arrow to layout
        arrow_layout.addWidget(self.possession_label)
        arrow_layout.addWidget(self.arrow_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        grid_layout.addWidget(arrow_widget, 2, 1)
         # Use Clutch Stats Toggle
        self.clutch_stats_checkbox = QCheckBox("Use Clutch Stats")
        self.clutch_stats_checkbox.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        self.clutch_stats_checkbox.setStyleSheet("color: white;")
        self.clutch_stats_checkbox.setToolTip("Use advanced clutch-time performance metrics for simulation.")
        grid_layout.addWidget(self.clutch_stats_checkbox, 2, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)



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
        player_team_id = self.simulation_screen.player_team['id']
        cpu_team_id = self.simulation_screen.cpu_team['id']

        #set teams scores
        use_clutch = self.clutch_stats_checkbox.isChecked()
        self.simulation_screen.set_game_variables(self.player_score_box.value(), self.cpu_score_box.value(), use_clutch) 

        # Open lineup selection window
        self.lineup_window = LineupSelectionWindow(player_team_id, cpu_team_id, self.lineup_set)
        self.lineup_window.show()

        print(f"Player's Team = {self.simulation_screen.player_team}")
        print(f"CPU's Team = {self.simulation_screen.cpu_team}")
        print(f"Player's Score = {self.player_score_box.value()}")
        print(f"CPU's Score = {self.cpu_score_box.value()}")

        #update logos
        self.simulation_screen.update_team_logos()
    
    def lineup_set(self, player_selected_players, cpu_lineup):
        print("Selected Players: ", player_selected_players)

        self.simulation_screen.set_player_lineup(player_selected_players)
        self.simulation_screen.set_cpu_lineup(cpu_lineup)
        self.simulation_screen.set_player_actions()
        

        # Switch to index 1: SimulationScreen
        self.stacked_widget.setCurrentIndex(1)  


    #selects player team
    def player_team_changed(self):
        selected_team = self.player_team_select.currentText()
        self.simulation_screen.update_player_team(selected_team)

    def cpu_team_changed(self):
        selected_team = self.cpu_team_select.currentText()
        self.simulation_screen.update_cpu_team(selected_team)

    def toggle_arrow(self):
        if self.current_direction == "left":
            self.arrow_button.setText(self.arrow_right)
            self.current_direction = "right"
            self.simulation_screen.game_info.set_possession(1)
        else:
            self.arrow_button.setText(self.arrow_left)
            self.current_direction = "left"
            self.simulation_screen.game_info.set_possession(0)



class LineupSelectionWindow(QWidget):
    def __init__(self, player_team_id, cpu_team_id, callback_function):
        super().__init__()

        #intialize variables
        self.player_team_id = player_team_id
        self.cpu_team_id = cpu_team_id
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
        roster = commonteamroster.CommonTeamRoster(team_id=player_team_id, season='2024-25')
        df = roster.get_data_frames()[0]
        self.player_names = list(df['PLAYER'])

        #need to get starting lineup for team
        player_starters = self.get_starters(self.player_team_id)

        #get starters for cpu team
        self.cpu_starters = self.get_starters(self.cpu_team_id)
        #print(f"CPU Starters = {self.cpu_starters}")

        # 5 dropdown menus for 5 players on the floor and
        for i in range(5):
            dropdown = QComboBox()
            dropdown.addItems(self.player_names)

            # set default from last game's starting lineup
            dropdown.setCurrentText(player_starters[i])

            self.dropdowns.append(dropdown)         # Adds dropdown value to list
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
        player_selected_players = [dropdown.currentText() for dropdown in self.dropdowns]

        if len(set(player_selected_players)) < 5:
            QMessageBox.warning(self, "Error", "You selected duplicate players!")
            return

        self.callback(player_selected_players, self.cpu_starters)  # Send selected players back to main app
        self.close() #close window

    # Get starters for default lineup
    def get_starters(self, team_id):
        season = '2024' 
        team = next((team['abbreviation'] for team in teams.get_teams() if team['id'] == team_id), None) # get abbreivation from team_id

        # Get regular season game log
        gamelog_regular = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season')
        games_regular = gamelog_regular.get_data_frames()[0]

        # Get playoff game log
        gamelog_playoffs = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Playoffs')
        games_playoffs = gamelog_playoffs.get_data_frames()[0]

        # Combine into one data frame
        games_combined = pd.concat([games_regular, games_playoffs], ignore_index=True)

        # Sort the combined games by GAME_DATE to get the most recent game
        games_combined['GAME_DATE'] = pd.to_datetime(games_combined['GAME_DATE'])  # first ahave to convert to datatime format
        games_combined_sorted = games_combined.sort_values(by='GAME_DATE', ascending=False)


        for game in games_combined_sorted.itertuples():
            game_id = game.Game_ID
            print(f"Checking Game ID: {game_id}")

            # Try to request game info
            try:
                boxscore_data = request_data(f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json")
            except Exception as e:
                print(f"Failed request for {game_id}: {e}")
                continue
            
            # Use get so program does not crash if missing
            game_data = boxscore_data.get("game", {})

            # Get home team name
            home_tricode = game_data.get("homeTeam", {}).get("teamTricode", {})

            # Select team
            which_team = "homeTeam" if home_tricode == team else "awayTeam"

            # Select players
            players = game_data.get(which_team, {}).get("players", [])

            # Select starters
            team_starters = [ 
                p for p in players if str(p.get("starter")) == "1" # Use str() for safety
            ]

            # Continue to next game if not starters listed
            if not team_starters:
                continue

            starters_list = [p.get("name") for p in team_starters]

            print(f"Found starters for Game ID: {game_id}")
            for player in team_starters:
                print(player['name'], player['position'])

            return starters_list
            
        print(f"No valid starters found in the recent games for {team}.")
        return






        # # Get most recent game
        # if not games_combined_sorted.empty:
        #     for _, game in games_combined_sorted.iterrows():            
                
        #         home_tricode = boxscore_data["game"]["homeTeam"]["teamTricode"]
                
        #         # Check teamm
        #         if home_tricode == team:
        #             which_team = "homeTeam"
        #         else:
        #             which_team = "awayTeam"

        #         # Get starters
        #         team_starters = [ 
        #                 player for player in boxscore_data["game"][which_team]["players"] if player["starter"] == "1"
        #             ]

        #         starters_list = [player['name'] for player in team_starters]

        #         print(starters_list)

        #         if starters_list:
        #             print(f"Found starters for Game ID: {game_id}")
        #             for player in team_starters:
        #                 print(player['name'], player['position'])
        #             return starters_list

        #     else:
        #         print(f"No valid starters found in the recent games for {team}.")
        #         return
        # else:
        #     print(f"No games found for {team}.")
        #     return