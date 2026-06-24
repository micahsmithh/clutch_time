import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerClutchSplits

# specify player by name
class Player:
    def __init__(self, player_name, df):
        self.name = player_name
        player_info = players.find_players_by_full_name(player_name)
        self.id = player_info[0]['id']
        self.clutch_stats = df[df['PLAYER_ID'] == self.id]

        print(self.clutch_stats[['PLAYER_NAME', 'FG_PCT', 'FG3_PCT']])



class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.playing = []
        self.players = []


        

    def set_lineup(self, player_list):
        self.playing = player_list

        
        #fetch all players on team