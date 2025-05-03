from nba_api.stats.endpoints import LeagueDashPlayerClutch, leaguedashplayerstats
import pandas as pd
from nba_api.stats.static import players

# Pull all player clutch stats
clutch_stats = LeagueDashPlayerClutch(
    season='2024-25',
    season_type_all_star='Regular Season',
    clutch_time='Last 5 Minutes', 
    ahead_behind='Ahead or Behind', 
    point_diff=5 
)

# Get data frame
df = clutch_stats.get_data_frames()[0]

# Now you can filter for a single player

#print(player_clutch[['PLAYER_NAME', 'FG3_PCT']])




class Player:
    def __init__(self, player_name, df):
        self.name = player_name
        player_info = players.find_players_by_full_name(player_name)
        self.id = player_info[0]['id']
        self.clutch_stats = df[df['PLAYER_ID'] == self.id]
    
        print(self.clutch_stats.iloc[0]['FG_PCT'])
        print(self.clutch_stats[['PLAYER_NAME', 'FG_PCT', 'FG3_PCT', 'FT_PCT']])



player_1 = Player('Darius Garland', df)