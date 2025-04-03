import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

class NBAStatsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NBA Player Stats")
        self.setGeometry(100, 100, 400, 350)

        self.layout = QVBoxLayout()

        # Input field for player name
        self.player_input = QLineEdit()
        self.player_input.setPlaceholderText("Enter Player Name (e.g., LeBron James)")

        # Button to fetch player stats
        self.fetch_button = QPushButton("Get Player Stats")
        self.fetch_button.clicked.connect(self.get_player_stats)

        # Label to display stats
        self.stats_label = QLabel("Player stats will appear here.")

        # Add widgets to layout
        self.layout.addWidget(self.player_input)
        self.layout.addWidget(self.fetch_button)
        self.layout.addWidget(self.stats_label)

        self.setLayout(self.layout)

    def get_player_stats(self):
        """Fetches and displays a player's current season stats."""
        player_name = self.player_input.text().strip()
        if not player_name:
            self.stats_label.setText("Please enter a player name!")
            return

        player = players.find_players_by_full_name(player_name)
        if not player:
            self.stats_label.setText("Player not found!")
            return
        
        player_id = player[0]['id']
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career.get_data_frames()[0]  # Convert API data to DataFrame

        # Get the most recent season stats
        latest_season = df.iloc[-1]  # Last row contains the latest season

        # Extract stats
        season = latest_season['SEASON_ID']
        gp = latest_season['GP']
        ppg = latest_season['PTS'] / gp if gp > 0 else 0
        apg = latest_season['AST'] / gp if gp > 0 else 0
        rpg = latest_season['REB'] / gp if gp > 0 else 0
        spg = latest_season['STL'] / gp if gp > 0 else 0
        bpg = latest_season['BLK'] / gp if gp > 0 else 0

        # Shooting percentages
        fg_pct = latest_season['FG_PCT'] * 100 if 'FG_PCT' in latest_season else 0
        tp_pct = latest_season['FG3_PCT'] * 100 if 'FG3_PCT' in latest_season else 0
        ft_pct = latest_season['FT_PCT'] * 100 if 'FT_PCT' in latest_season else 0

        # Update UI with stats
        self.stats_label.setText(
            f"{player_name} ({season}):\n"
            f"PPG: {ppg:.1f} | APG: {apg:.1f} | RPG: {rpg:.1f}\n"
            f"FG%: {fg_pct:.1f}% | 3P%: {tp_pct:.1f}% | FT%: {ft_pct:.1f}%\n"
            f"SPG: {spg:.1f} | BPG: {bpg:.1f}"
        )

# Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NBAStatsApp()
    window.show()
    sys.exit(app.exec())
