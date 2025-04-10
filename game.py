import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import random

class game:
    def __init__(self, player_score, cpu_score, possession):
        self.player_score = player_score
        self.cpu_score = cpu_score
        self.play_clock = 60        #60 seconds
        self.possession = possession
    
    def set_player_score(self, score):
        self.player_score = score

    def set_cpu_score(self, score):
        self.cpu_score = score

    def set_possession(self, possession):
        self.possession = possession
