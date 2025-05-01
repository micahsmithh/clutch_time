import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import random

class game:
    def __init__(self, player_score=0, cpu_score=0, possession=None):
        self.player_score = player_score
        self.cpu_score = cpu_score
        self.play_clock = 60        #60 seconds
        self.shot_clock = 24
        self.possession = 0 # 0 will represnt player possession and 1 will represent cpu possession
    
    def set_player_score(self, score):
        self.player_score = score

    def set_cpu_score(self, score):
        self.cpu_score = score

    def set_play_clock(self, time):
        self.play_clock = time
    
    def set_shot_clock(self, time):
        self.shot_clock = time

    def set_possession(self, possession):
        self.possession = possession
