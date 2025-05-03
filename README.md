# clutch_time
Clutch Time Basketball Simulator

## Installation
For this project, I used three different python libraries which can be installed via "pip install". These libraries are PyQt6, nba_api, and pandas. 

Pyqt6  was used to create the UI. nba_api was used to access and interact with the official NBA data being used suchas real times teams, players, and stats. Pandas was used to manipulate some of the data sets from nba_api I was using.

To run the simulation just two files are needed: the main_ui.py and game.py files

Tha main_ui.py file has the the three classes for the three screens (The StartScreen, LineupSelectionWindow and SimulatioScreen) as well as the MainWindow class which holds the stacked_widget which is the central widget.

The game.py file holds the Game class which holds important variables used in the game

## Other Files
In the nba_images folder is the two images which are used in the simulation

The other .py files were all used for testing different functionalities of the nba_api and have changed throughout the testing and design process
