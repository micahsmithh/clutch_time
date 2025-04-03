import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.player_name = 



class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.playing = []
        self.players = []


        

    def set_lineup(self, player_list):
        self.playing = player_list

        
        #fetch all players on team