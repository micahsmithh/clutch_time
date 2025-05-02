from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QStackedWidget, QComboBox, QVBoxLayout, QSpinBox, QMessageBox, QHBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtGui import QFont, QPixmap, QPainter, QIntValidator, QValidator, QFontDatabase, QFont 
from PyQt6.QtCore import Qt, QByteArray
from nba_api.stats.endpoints import TeamEstimatedMetrics, teamgamelog, boxscoretraditionalv2, LeagueDashPlayerClutch, LeagueDashPlayerStats
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonteamroster
import pandas as pd
from game import game
import requests, random, sys

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
        self.simulation_screen.set_game_variables(self.player_score_box.value(), self.cpu_score_box.value()) 

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
        roster = commonteamroster.CommonTeamRoster(team_id=player_team_id)
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

    def get_starters(self, team_id):
        season = '2024' 
        team = next((team['abbreviation'] for team in teams.get_teams() if team['id'] == team_id), None) # get abbreivation from team_id

        # Fetch the regular season game log
        gamelog_regular = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season')
        games_regular = gamelog_regular.get_data_frames()[0]

        # Fetch the playoff game log
        gamelog_playoffs = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Playoffs')
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
        self.game_info = game()

        self.player_lineup = []
        self.cpu_lineup = []
        self.player_stats = {}
        self.cpu_stats = {}
        self.player_team_stats = {}
        self.cpu_team_stats = {}

        layout = QGridLayout()
        self.setLayout(layout)


        # label = QLabel("🏀 Simulation Screen 🏀")
        # label.setFont(QFont("Helvetica", 30, QFont.Weight.Bold))
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(label, 0, 0, 1, 2)

        # Back Button (Switch back to Start Screen)
        back_button = QPushButton("Exit Simulation")
        back_button.setFont(QFont("Helvetica", 14))
        back_button.setStyleSheet("background-color: red; color: white; padding: 10px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_button, 3, 0, 1, 4)



        ##################################
        # Setting Up Main UI Elements
        ##################################
        
        # Lineups and Play Log
        self.left_lineup = QVBoxLayout()    # Player team lineup
        self.center_log = QVBoxLayout()     # Play-by-play log
        self.right_lineup = QVBoxLayout()   # CPU team lineup

        #holds lineup lables
        self.player_lineup_labels = []
        self.cpu_lineup_labels = []


        # Fill player lineup

        for i in range(5):
            player_layout = QHBoxLayout()

            image_label = QLabel()  # Set headshot label
            image_label.setFixedSize(50, 50)
            

            text_label = QLabel(f"Player {i+1}")        #text label
            text_label.setFont(QFont("Helvetica", 13))
            text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            player_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignVCenter)    # Add headshot image first
            player_layout.addWidget(text_label)     # Player name next to image
            self.left_lineup.addLayout(player_layout)   # Add layout to overall lineup layout

            self.player_lineup_labels.append((image_label, text_label))

        # Fill CPU lineup
        for i in range(5):
            player_layout = QHBoxLayout()

            image_label = QLabel()  # Set headshot label
            image_label.setFixedSize(50, 50)
            
            

            text_label = QLabel(f"Player {i+1}")        #text label
            text_label.setFont(QFont("Helvetica", 13))
            text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            player_layout.addWidget(image_label)    # Add headshot image first
            player_layout.addWidget(text_label)     # Player name next to image
            self.right_lineup.addLayout(player_layout)   # Add layout to overall lineup layout

            self.cpu_lineup_labels.append((image_label, text_label))

        # Play log label (scrollable)
        self.play_log = QTextEdit()
        self.play_log.setReadOnly(True)
        self.play_log.setFont(QFont("Helvetica", 12))
        log_title = QLabel("Play by Play")
        log_title.setFont(QFont("Helvetica", 15, QFont.Weight.Bold))
        self.center_log.addWidget(log_title)
        self.center_log.addWidget(self.play_log)

        self.left_lineup_widget = QWidget()
        self.left_lineup_widget.setLayout(self.left_lineup)
        self.left_lineup_widget.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);  /* semi-transparent black */
            border-radius: 10px;
            padding: 2px;
        """)

        self.right_lineup_widget = QWidget()
        self.right_lineup_widget.setLayout(self.right_lineup)
        self.right_lineup_widget.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);  /* semi-transparent black */
            border-radius: 10px;
            padding: 2px;
        """)

        # Add to the main grid layout 
        layout.addLayout(self.center_log, 1, 2, 2, 1)   # spans 2 rows 1 columns
        layout.addLayout(self.left_lineup, 1, 0, 1, 1)
        layout.addWidget(self.left_lineup_widget, 1, 0, 1, 1)
        layout.addLayout(self.right_lineup, 1, 3, 1, 1)
        layout.addWidget(self.right_lineup_widget, 1, 3, 1, 1)

        ###############################
        # SCOREBOARD
        ###############################

        font_id = QFontDatabase.addApplicationFont("fonts/digital-7.TTF")  # path to .ttf file
        family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # Add logos
        self.player_logo = QLabel()
        layout.addWidget(self.player_logo, 0, 0)

        self.cpu_logo = QLabel()
        layout.addWidget(self.cpu_logo, 0, 2)

       # Scoreboard Container
        scoreboard_widget = QWidget()
        scoreboard_layout = QHBoxLayout()
        scoreboard_layout.setContentsMargins(10, 10, 10, 10)
        scoreboard_widget.setLayout(scoreboard_layout)
        
        # Setting Color and Radius
        scoreboard_widget.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            border-radius: 15px;
        """)

        # ----------- PLAYER SIDE -------------
        left_box = QVBoxLayout()

        you_label = QLabel("YOU")
        you_label.setStyleSheet("color: white; font-size: 16px;")
        you_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.player_logo = QLabel()
        self.player_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.player_logo.setStyleSheet("background-color: transparent;")

        self.player_score = QLabel("0")
        self.player_score.setStyleSheet("""
            background-color: white;
            color: black;
            font-size: 18px;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 8px;
        """)
        self.player_score.setAlignment(Qt.AlignmentFlag.AlignCenter)               

        left_box.addWidget(you_label)
        left_box.addWidget(self.player_logo)
        left_box.addWidget(self.player_score)

        # ----------- Middle -------------
        center_box = QVBoxLayout()

        time_label = QLabel("TIME")
        time_label.setStyleSheet("color: white; font-size: 16px;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clock_display = QLabel("1:00 Q4")
        self.clock_display.setStyleSheet("""
            color: rgb(255, 255, 51);
            font-size: 30px;
            padding: 4px 12px;
            border-radius: 8px;
        """)
        self.clock_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Shot Clock Label
        self.shot_clock_display = QLabel("24")
        self.shot_clock_display.setStyleSheet("""
            color: red;
            font-size: 30px;
            padding: 4px 12px;
            border-radius: 8px;
        """)
        self.shot_clock_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shot_clock_display.setFixedWidth(60)
        self.shot_clock_display.setFixedHeight(60)

        
        self.clock_display.setFont(QFont(family))
        self.shot_clock_display.setFont(QFont(family))
        

        #center_box.addWidget(time_label)
        center_box.addWidget(self.clock_display)
        center_box.addWidget(self.shot_clock_display)
        center_box.setAlignment(self.shot_clock_display, Qt.AlignmentFlag.AlignHCenter)

        # ----------- CPU SIDE -------------
        right_box = QVBoxLayout()

        cpu_label = QLabel("CPU")
        cpu_label.setStyleSheet("color: white; font-size: 16px;")
        cpu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cpu_logo = QLabel()
        self.cpu_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cpu_logo.setStyleSheet("background-color: transparent;")

        self.cpu_score = QLabel("0")
        self.cpu_score.setStyleSheet("""
            background-color: white;
            color: black;
            font-size: 18px;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 8px;
        """)
        self.cpu_score.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_box.addWidget(cpu_label)
        right_box.addWidget(self.cpu_logo)
        right_box.addWidget(self.cpu_score)

        # Add all three to scoreboard layout
        scoreboard_layout.addLayout(left_box)
        scoreboard_layout.addStretch()
        scoreboard_layout.addLayout(center_box)
        scoreboard_layout.addStretch()
        scoreboard_layout.addLayout(right_box)

        # Place scoreboard at the top center of the grid
        layout.addWidget(scoreboard_widget, 0, 1, 1, 2)

        ###############################
        # GAME ACTIONS
        ###############################

        # Player Action Container
        player_action_widget = QWidget()
        player_action_layout = QVBoxLayout()
        player_action_layout.setContentsMargins(5, 5, 5, 5)
        player_action_widget.setLayout(player_action_layout)

        player_action_widget.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            border-radius: 5px;
        """)

        # Player Actions Dropdowns
        self.player_select = QComboBox()
        self.player_actions = QComboBox()

        self.clock_used = QLineEdit()
        self.clock_used.setFont(QFont("Helvetica", 12))
        self.validator = QIntValidator(1, self.game_info.shot_clock)
        self.clock_used.setValidator(self.validator)
        self.clock_used.setPlaceholderText("Clock Used (seconds)")
        self.clock_used.textChanged.connect(self.clock_used_entered)

        # Sim Button
        self.sim_button = QPushButton("Sim")
        self.sim_button.setFont(QFont("Helvetica", 12))
        self.sim_button.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
            QPushButton:pressed {
                background-color: lightgreen;
                color: black;
            }
        """)
        self.sim_button.clicked.connect(self.sim_button_clicked)  #will start simulation

        # Label for Actions
        self.player_action_text = QLabel("Offensive Action")
        self.player_action_text.setFont(QFont("Helvetica", 13))
        self.player_action_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add Widgets to Player Action Layout
        player_action_layout.addWidget(self.player_action_text)
        player_action_layout.addWidget(self.player_actions)
        player_action_layout.addWidget(self.player_select)
        player_action_layout.addWidget(self.clock_used)
        player_action_layout.addWidget(self.sim_button)
        


        layout.addWidget(player_action_widget, 1, 1, 1, 1)

    #update selected teams (called from start) and sets variable to dictionary
    def update_player_team(self, player_team):
        self.player_team = teams.find_teams_by_full_name(player_team)[0]

        #gonna have to update text labels
    def update_cpu_team(self, cpu_team):
        self.cpu_team = teams.find_teams_by_full_name(cpu_team)[0]
        #gonna have to update text labels

        #print(f"Abbreviation: {self.cpu_team[0]['abbreviation']}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    def set_player_lineup(self, player_lineup):
        self.player_lineup = player_lineup
        for i, name in enumerate(player_lineup):
            image_label, text_label = self.player_lineup_labels[i]  # Access both the image and text
            text_label.setText(name)
            
            # Fetch headshot
            player_info = players.find_players_by_full_name(name)
            player_id = player_info[0]['id']
            headshot_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
            pixmap = self.get_image_from_url(headshot_url)

            # Set pixmap 
            scaled_pixmap = pixmap.scaled(
                50, 50,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(scaled_pixmap)


        print(f"Player's Lineup: {self.player_lineup}")
        self.player_stats = self.get_regular_season_dict(player_lineup) # Put stats in our own dictionary
        self.player_team_stats = self.get_team_stats_dict(self.player_team['full_name']) # Put team stats in dictionary
        #print(f"{self.player_team['full_name']}'s stats are : {self.player_team_stats}")


    def set_cpu_lineup(self, cpu_lineup):
        self.cpu_lineup = cpu_lineup
        for i, name in enumerate(cpu_lineup):
            image_label, text_label = self.cpu_lineup_labels[i]  # Access both the image and text
            text_label.setText(name)
            
            # Fetch headshot
            player_info = players.find_players_by_full_name(name)
            player_id = player_info[0]['id']
            headshot_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
            pixmap = self.get_image_from_url(headshot_url)

            # Set pixmap 
            scaled_pixmap = pixmap.scaled(
                50, 50,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode=Qt.TransformationMode.SmoothTransformation
            )
            image_label.setPixmap(scaled_pixmap)

        print(f"CPU's Lineup: {self.cpu_lineup}")
        self.cpu_stats = self.get_regular_season_dict(cpu_lineup) # Put stats in our own dictionary
        self.cpu_team_stats = self.get_team_stats_dict(self.cpu_team['full_name'])
        #print(f"{self.cpu_team['full_name']}'s stats are : {self.cpu_team_stats}")

    def update_team_logos(self):
        
        # player_name = "Donovan Mitchell"
        # player_info = players.find_players_by_full_name(player_name)
        # player_id = player_info[0]["id"]
        # headshot_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"

        #url we will pull logo from
        abbreviation = None

        if self.player_team['abbreviation'] == 'UTA':
            abbreviation = 'UTH'
        elif self.player_team['abbreviation'] == 'NOP':
            abbreviation = 'NOR'
        else:
            abbreviation = self.player_team['abbreviation']

        logo_url = f"https://a.espncdn.com/i/teamlogos/nba/500/{abbreviation}.png"

        pixmap = self.get_image_from_url(logo_url)
        scaled_pixmap = pixmap.scaled(
            80, 80,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        self.player_logo.setPixmap(scaled_pixmap)
        self.player_logo.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #now we do same thing with cpu_team
        if self.cpu_team['abbreviation'] == 'UTA':
            abbreviation = 'UTH'
        elif self.cpu_team['abbreviation'] == 'NOP':
            abbreviation = 'NOR'
        else:
            abbreviation = self.cpu_team['abbreviation']

        logo_url = f"https://a.espncdn.com/i/teamlogos/nba/500/{abbreviation}.png"

        pixmap = self.get_image_from_url(logo_url)
        scaled_pixmap = pixmap.scaled(
            80, 80,
            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
            transformMode=Qt.TransformationMode.SmoothTransformation
        )
        self.cpu_logo.setPixmap(scaled_pixmap)
        self.cpu_logo.setAlignment(Qt.AlignmentFlag.AlignRight)


            

    #set scores
    def set_game_variables(self, player_score, cpu_score):
        self.game_info.set_player_score(player_score)
        self.game_info.set_cpu_score(cpu_score)
        self.play_log.clear()
        self.game_info.set_game_clock(60)
        self.game_info.set_shot_clock(24)
        self.update_scoreboard()

        # print(self.game_info.player_score)
        # print(self.game_info.cpu_score)

    # Returns pixmap from URL
    def get_image_from_url(self, url):

        response = requests.get(url)

        #check to see if pull is successful
        if response.status_code == 200:
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(image_data))
            return pixmap   #return pixmap
        else:
            print("Failed to Load image from URL")


    def get_clutch_dict(self, players_list):

        # pull clutch stats
        clutch_stats = LeagueDashPlayerClutch(
        season='2024-25',
        season_type_all_star='Regular Season',
        clutch_time='Last 5 Minutes', 
        ahead_behind='Ahead or Behind', 
        point_diff=5  # within 5 points
        )

        # Get Data Frame
        df = clutch_stats.get_data_frames()[0]

        clutch_dict = {}

        print(f"Team : {players_list}")

        for name in players_list:
            player_info = players.find_players_by_full_name(name)

            # Error Checking Names
            if not player_info:
                print(f"Player {name} not found")
                continue

            player_id = player_info[0]['id']
            player_clutch_stats = df[df['PLAYER_ID'] == player_id]

            # Error Checking Stats
            if player_clutch_stats.empty:
                print(f"Season stats not found for {name}")
                continue

            # calculate FG2_PCT
            #print(player_clutch_stats.iloc[0]['FGA'])

            two_points_attempted = player_clutch_stats.iloc[0]['FGA'] - player_clutch_stats.iloc[0]['FG3A']
            two_points_made = player_clutch_stats.iloc[0]['FGM'] - player_clutch_stats.iloc[0]['FG3M']
            two_point_percentage = round(two_points_made / two_points_attempted, 3) if two_points_attempted != 0 else 0 #zero checking

            clutch_dict[name] = {
                'FG_PCT' : player_clutch_stats.iloc[0]['FG_PCT'],
                'FG3_PCT' : player_clutch_stats.iloc[0]['FG3_PCT'],
                'FG2_PCT' : two_point_percentage,
                'FT_PCT'  : player_clutch_stats.iloc[0]['FT_PCT']
            
        }
            
        # print(f"{players_list[0]}'s FG_PCT = {clutch_dict[players_list[0]]['FG_PCT']}")
        # print(f"{players_list[0]}'s FG2_PCT = {clutch_dict[players_list[0]]['FG2_PCT']}")
        # print(f"{players_list[0]}'s FG3_PCT = {clutch_dict[players_list[0]]['FG3_PCT']}")
        # print(f"{players_list[0]}'s FT_PCT = {clutch_dict[players_list[0]]['FT_PCT']}")

        return clutch_dict

    

    def get_regular_season_dict(self, players_list):
        # Pull regular season player stats
        regular_stats = LeagueDashPlayerStats(
            season='2024-25',
            season_type_all_star='Regular Season'
        )

        # Get Data Frame
        df = regular_stats.get_data_frames()[0]

        player_stats_dict = {}

        print(f"Team : {players_list}")

        for name in players_list:
            player_info = players.find_players_by_full_name(name)

            # Error Checking Names
            if not player_info:
                print(f"Player {name} not found")
                continue

            player_id = player_info[0]['id']
            player_season_stats = df[df['PLAYER_ID'] == player_id]

            # Error Checking Stats
            if player_season_stats.empty:
                print(f"Season stats not found for {name}")
                continue

            # calculate FG2_PCT
            #print(player_season_stats.iloc[0]['FGA'])

            two_points_attempted = player_season_stats.iloc[0]['FGA'] - player_season_stats.iloc[0]['FG3A']
            two_points_made = player_season_stats.iloc[0]['FGM'] - player_season_stats.iloc[0]['FG3M']
            two_point_percentage = round(two_points_made / two_points_attempted, 3) if two_points_attempted != 0 else 0 # zero checking

            player_stats_dict[name] = {
                'FG_PCT' : player_season_stats.iloc[0]['FG_PCT'],
                'FG3_PCT' : player_season_stats.iloc[0]['FG3_PCT'],
                'FG2_PCT' : two_point_percentage,
                'FT_PCT'  : player_season_stats.iloc[0]['FT_PCT']
            
        }

        return player_stats_dict




    
    def get_team_stats_dict(self, team_name):
        # Define parameters
        season = '2024-25' 
        season_type = 'Regular Season'

        # Call the endpoint
        stats = TeamEstimatedMetrics(season=season, season_type=season_type)

        # Get the data frame
        df = stats.get_data_frames()[0]

        # Filter for team
        team_row = df[df['TEAM_NAME'] == team_name]
        
        # Get E_TM_TOV_PCT
        if not team_row.empty:
            team_stats_dict = {
                'TOV_PCT' : team_row.iloc[0]['E_TM_TOV_PCT'],
                'OREB_PCT' : team_row.iloc[0]['E_OREB_PCT'],
                'DREB_PCT' : team_row.iloc[0]['E_DREB_PCT'],
            } 
            print(f"{team_name} stats {team_stats_dict}")
            return team_stats_dict
        elif team_name == "Los Angeles Clippers":
            team_row = df[df['TEAM_NAME'] == "LA Clippers"]

            team_stats_dict = {
                'TOV_PCT' : team_row.iloc[0]['E_TM_TOV_PCT'],
                'OREB_PCT' : team_row.iloc[0]['E_OREB_PCT'],
                'DREB_PCT' : team_row.iloc[0]['E_DREB_PCT'],
            } 
            print(f"LA Clippers stats {team_stats_dict}")
            return team_stats_dict
        else:
            print(f"{team_name} data not found")

    #update scoreborard
    def update_scoreboard(self):
        self.player_score.setText(str(self.game_info.player_score))
        self.cpu_score.setText(str(self.game_info.cpu_score))

        # Update Shot Clock
        self.shot_clock_display.setText(str(self.game_info.shot_clock))

        # Update Game Clock
        if self.game_info.game_clock < 10:
            self.clock_display.setText(f"00:0{self.game_info.game_clock} Q4")
        elif self.game_info.game_clock < 60:
            self.clock_display.setText(f"00:{self.game_info.game_clock} Q4")
        else:
            self.clock_display.setText(f"01:00 Q4")

    def set_player_actions(self):

        # Clear Selections First
        self.player_select.clear()
        self.player_actions.clear()
                
        # if player possession(0), sets according widgets
        if self.game_info.possession == 0:
            self.player_action_text.setText("Offensive Action")

            self.player_select.addItem("Select Shooter")
            self.player_select.addItems(self.player_lineup) # Add player's players

            self.player_actions.addItem("Choose Offensive Play")
            self.player_actions.addItems(["Shoot a Two", "Shoot a Three"])
        else:
            self.player_action_text.setText("Defensive Action")

            self.player_select.addItem("Select Player to Foul")
            self.player_select.addItems(self.cpu_lineup) # Add CPU's player

            self.player_actions.addItem("Choose Defensive Play")
            self.player_actions.addItems(["Foul", "No Foul"])

        # Enable Buttons
        self.sim_button.setEnabled(True)
        self.player_select.setEnabled(True)
        self.player_actions.setEnabled(True)
        self.clock_used.setEnabled(True)
        

        self.clock_used.clear()
        self.clock_used.setStyleSheet("")
        self.clock_used.setValidator(QIntValidator(0, self.game_info.shot_clock if self.game_info.shot_clock < self.game_info.game_clock else self.game_info.game_clock))

        self.player_select.model().item(0).setEnabled(False)
        self.player_actions.model().item(0).setEnabled(False)

    def clock_used_entered(self):
        print(f"shot clock = {self.game_info.shot_clock}")
        self.validator = QIntValidator(1, self.game_info.shot_clock)
        text = self.clock_used.text()
        state = self.validator.validate(text, 0)[0]
        if state != QValidator.State.Acceptable:
            self.clock_used.setStyleSheet("border: 2px solid red;")
            print("Invalid Input")
        else:
            self.clock_used.setStyleSheet("")
            print(f"Valid Input ")
    
    def sim_button_clicked(self):
        print(self.player_team)

        player_action = self.player_actions.currentText()

        # Check Clock
        text = self.clock_used.text()
        state = self.validator.validate(text, 0)[0]
        shooter = self.player_select.currentText()

        # Don't need Time if No Foul is Selected
        if player_action != "No Foul":
            if state == QValidator.State.Acceptable:
                print(f"Time Burned = {int(text)}")
            else:
                QMessageBox.warning(self, "Error", "Please Select Time to Come off Clock")
                return

        # Offensive Possession
        if self.game_info.possession == 0:

            # Check Offensive Player
            if shooter in self.player_lineup:
                print(f"Shooter is {shooter}")
            else:
                QMessageBox.warning(self, "Error", "Please Select Shooter")
                return
                

            # Check offensive action
            match player_action:
                case "Shoot a Two":
                    print ("Two")
                    self.handle_offensive_action("two", shooter, int(text))
                case "Shoot a Three":
                    print ("Three")
                    self.handle_offensive_action("three", shooter, int(text))
                # case "Call Timeout":
                #     print("Timeout")
                case _:
                    QMessageBox.warning(self, "Error", "Select Offensive Action")
                    return
        # Defensive Possession       
        else:
            # Check Defensive Play
            if player_action == "No Foul":
                print("No Foul")
                self.handle_defensive_action(player_action, shooter, 100) # Set to 100 just to not mess with defensive handling
            elif player_action == "Foul":
                player = self.player_select.currentText()

                # Check Player being Fouled
                if player in self.cpu_lineup:
                    print(f"Fouling {player}")
                    self.handle_defensive_action(player_action, shooter, int(text))
                else:
                    QMessageBox.warning(self, "Error", "Please Select Player to Foul")
                    return
            else:
                QMessageBox.warning(self, "Error", "Please Select Defensive Action")
                return
                    


    def log_play(self, play):
        if self.game_info.game_clock < 10:
            self.play_log.append(f"00:0{self.game_info.game_clock}: {play}")
        else:
            self.play_log.append(f"00:{self.game_info.game_clock}: {play}")

    def handle_offensive_action(self, action, player, time):
        
        # Put time high unless needs to be changed
        cpu_time = 100
        score_diff = self.game_info.player_score-self.game_info.cpu_score

        if self.game_info.shot_clock >= self.game_info.game_clock-3 and score_diff > 0 and score_diff < 6:  # CPU down less than 6 with shot clock off or 3 second difference
            if self.game_info.shot_clock > 15:
                cpu_time = random.randint(3, 13)
            elif self.game_info.shot_clock > 10 and score_diff < 4: 
                cpu_time = random.randint(1, 5)
            elif self.game_info.shot_clock > 5 and score_diff < 4: 
                cpu_time = random.randint(1, 4)
            elif self.game_info.shot_clock > 1 and score_diff < 4: 
                cpu_time = random.randint(1, self.game_info.shot_clock-1)

        if cpu_time <= time:
            # Check for turnover
            if self.handle_turnover(cpu_time):
                return

            self.game_info.game_clock -= cpu_time
            # Fet player to be fouled
            cpu_fouled_player = random.choice(self.player_lineup)
            cpu_fouled_player_stats = self.player_stats[cpu_fouled_player]
            self.log_play(f"{cpu_fouled_player} fouled")

            # Free Throw Logic
            if random.random() < cpu_fouled_player_stats['FT_PCT']:
                points = 1
                self.log_play(f"{cpu_fouled_player} makes free throw 1 of 2")
                self.game_info.player_score += points
                self.update_scoreboard()
            else:
                self.log_play(f"{cpu_fouled_player} misses free throw 1 of 2")
            
            # Second free throw
            if random.random() < cpu_fouled_player_stats['FT_PCT']:
                make = True
                points = 1
                self.log_play(f"{cpu_fouled_player} makes free throw 2 of 2")
                self.game_info.player_score += points 
            else:
                self.log_play(f"{cpu_fouled_player} misses free throw 2 of 2")
                make = False
        else: # Player Controlled Action Occurs
            # Calculate Time
            if time == self.game_info.game_clock or time == self.game_info.shot_clock:  # Run Clock Out
                self.game_info.game_clock -= time
                
                if self.game_info.game_clock <= 0:
                    self.game_over()
                    return
            else:
                # Check for turnover
                if self.handle_turnover(time):
                    return
                self.game_info.game_clock -= time
            
            stats = self.player_stats[player]
            make = False
            points = 0

            if action == "two":
                if random.random() < stats['FG2_PCT']:
                    make = True
                    points = 2
            elif action == "three":
                if random.random() < stats['FG3_PCT']:
                    make = True
                    points = 3
            else:
                print(f"Unknown Action: {action}")

            if make:
                self.log_play(f"{player} makes {action} point shot")

                # Update Scoreboard
                self.game_info.player_score += points 
            else:
                self.log_play(f"{player} misses {action} point shot")

        # Must handle rebounds and update scoreboard
        self.handle_rebound(make)
        self.update_scoreboard()

        # Check if timer is up
        print(f"Game Clock at: {self.game_info.game_clock}")
        if self.game_info.game_clock <= 0:
            self.game_over()

    def handle_defensive_action(self, action, player, time):

        # For easier access to variable checking
        p_score = self.game_info.player_score
        c_score = self.game_info.cpu_score
        shot_clock = self.game_info.shot_clock
        game_clock = self.game_info.game_clock

        # Cpu Variables
        cpu_shooter = random.choice(self.cpu_lineup)
        cpu_stats = self.cpu_stats[cpu_shooter]
        cpu_shot = None
        cpu_time = None
        points = 0

        # Fouling Time not Exact
        # if action == "Foul":
        #     if random.random() < .5:
        #         time += random.randint(0, 2)
        #     else:
        #         time -= random.randint(0, 2)

        # CPU logic
        if shot_clock >= game_clock and c_score > p_score:  # CPU up with shot clock off
            cpu_time = shot_clock
        elif c_score == p_score-3 and game_clock < 10:      # CPU down 3 under 10 seconds
            cpu_shot = "three"
            cpu_time = random.randint(1, game_clock)
        elif c_score > p_score:                             # CPU up 
            if random.random() < .5:
                cpu_shot = "three"
            else:
                cpu_shot = "two"
            cpu_time = random.randint(15, 23)
        elif c_score > p_score-3:                           # CPU down 2 or less or tied
            if random.random() < .5:
                cpu_shot = "three"
            else:
                cpu_shot = "two"

            if shot_clock > 23:
                cpu_time = random.randint(5, 23)
            else:
                cpu_time = random.randint(1, shot_clock)
        else:                                               # CPU down more than 3
            if random.random() < .5:
                cpu_shot = "three"
            else:
                cpu_shot = "two"
            if shot_clock > 15:
                cpu_time = random.randint(5, 15)
            else:
                cpu_time = random.randint(1, shot_clock)
        make = False

        # Compare time to cpu_time to see which action happens
        if time < cpu_time and action == "Foul": # Player Action Occurs (Free Throws)
            # Check for turnover
            if self.handle_turnover(time):
                return

            self.game_info.game_clock -= time
            stats = self.cpu_stats[player]
            self.log_play(f"{player} fouled")

            # First Free Throw
            if random.random() < stats['FT_PCT']:
                points = 1
                self.log_play(f"{player} makes free throw 1 of 2")
                self.game_info.cpu_score += points
                self.update_scoreboard()
            else:
                self.log_play(f"{player} misses free throw 1 of 2")
            
            # Second free throw
            if random.random() < stats['FT_PCT']:
                make = True
                points = 1
                self.log_play(f"{player} makes free throw 2 of 2")
                self.game_info.cpu_score += points 
            else:
                self.log_play(f"{player} misses free throw 2 of 2")
                make = False
        else:   # CPU Action Occurs
            # Check for turnover
            if self.handle_turnover(cpu_time):
                return

            self.game_info.game_clock -= cpu_time
            
            # Checkign Shot Type
            if cpu_shot == "two":
                if random.random() < cpu_stats['FG2_PCT']:
                    make = True
                    points = 2
            elif cpu_shot == "three":
                if random.random() < cpu_stats['FG3_PCT']:
                    make = True
                    points = 3
            else:                   # CPU took no shot (only should occur if they can run time to 0)
                if game_clock <= 0:
                    self.game_over()
                    return
            if make:
                self.log_play(f"{cpu_shooter} makes {cpu_shot} point shot")
                # Update Scoreboard
                self.game_info.cpu_score += points  
            else:
                self.log_play(f"{cpu_shooter} misses {cpu_shot} point shot")

        # Handle rebounds and update scoreboard
        self.handle_rebound(make)
        self.update_scoreboard()
        
        # Check if timer is up
        print(f"Game Clock at: {self.game_info.game_clock}")
        if self.game_info.game_clock <= 0:
            print("In da loop")
            self.game_over()


    def handle_rebound(self, make):
        if make:
            self.game_info.set_shot_clock(24)   # Reset Shot Clock
            self.game_info.set_possession(not(self.game_info.possession))   # Flip Possession
        else:
            # Probability of Offenesive Rebund = OREB% / (OREB% + Opponent DREB%)
            p_oreb = None
            o_team = None
            d_team = None
            if self.game_info.possession == 0:
                p_oreb = self.player_team_stats['OREB_PCT'] / (self.player_team_stats['OREB_PCT'] + self.cpu_team_stats['DREB_PCT'])
                o_team = self.player_team['nickname']
                d_team = self.cpu_team['nickname']
            else:
                p_oreb = self.cpu_team_stats['OREB_PCT'] / (self.cpu_team_stats['OREB_PCT'] + self.player_team_stats['DREB_PCT'])
                o_team = self.cpu_team['nickname']
                d_team = self.player_team['nickname']

            # Handle if Offensive Rebound Occurs

            print(f"Offensive Rebound chance: {p_oreb}")

            if random.random() < p_oreb:
                self.game_info.set_shot_clock(14)
                self.log_play(f"{o_team} offensive rebound")
            else:   # Defensive Rebound
                self.game_info.set_shot_clock(24)   # Reset Shot Clock
                self.game_info.set_possession(not(self.game_info.possession)) # Possession Changes
                self.log_play(f"{d_team} defensive rebound")

        self.set_player_actions()   # Set Player Actions

    def handle_turnover(self, time):
        p_tov = None # Probability of turnover
        o_team = None # Offensive Team


        if self.game_info.possession == 0:
            p_tov = self.player_team_stats['TOV_PCT']
            o_team = self.player_team['nickname']
        else:
            p_tov = self.cpu_team_stats['TOV_PCT']
            o_team = self.cpu_team['nickname']

        print(f"{o_team}'s  turnover chance: {p_tov}")

        if random.random() < p_tov: # Turnover Occurs

            # Clock
            time_used = random.randint(0, time)
            self.game_info.game_clock -= time_used
            self.game_info.set_shot_clock(24)   # Reset Shot Clock

            self.game_info.set_possession(not(self.game_info.possession)) # Flip possession
            self.log_play(f"{o_team} turnover")

            # Update UI
            self.set_player_actions() 
            self.update_scoreboard()

            return True
        else:  
            return False
    

    def handle_cpu_fouls(self):
        # First Free Throw
        cpu_time = 100
        cpu_fouled_player = random.choice(self.player_lineup)
        cpu_fouled_player_stats = self.player_stats[cpu_fouled_player]

        if self.game_info.shot_clock >= self.game_info.game_clock and self.game_info.player_score > self.game_info.cpu_score:  # CPU down with shot clock off
            if self.game_info.shot_clock > 15:
                cpu_time = random.randint(3, 13)
            else: 
                cpu_time = random.randint(1, self.game_info.shot_clock)


        if random.random() < cpu_fouled_player_stats['FT_PCT']:
            points = 1
            self.log_play(f"{cpu_fouled_player} makes free throw 1 of 2")
            self.game_info.cpu_score += points
            self.update_scoreboard()
        else:
            self.log_play(f"{cpu_fouled_player} misses free throw 1 of 2")
        
        # Second free throw
        if random.random() < cpu_fouled_player_stats['FT_PCT']:
            make = True
            points = 1
            self.log_play(f"{cpu_fouled_player} makes free throw 2 of 2")
            self.game_info.cpu_score += points 
        else:
            self.log_play(f"{cpu_fouled_player} misses free throw 2 of 2")
            make = False
        
            

    def game_over(self):
        self.game_info.set_shot_clock(0)
        self.update_scoreboard()
        self.log_play("Game Over")
        self.sim_button.setEnabled(False)
        self.player_select.setEnabled(False)
        self.player_actions.setEnabled(False)
        self.clock_used.setEnabled(False)



    # def run_simulation(self):

    #     # checks if player has possession
    #     if self.game_info.game_clock > 0:
        
    #     # Check for Overtime
    #     elif self.game_info.player_score == self.game_info.cpu_score:
            
             



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basketball Simulation")
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
