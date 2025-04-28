from nba_api.stats.endpoints import playergamelog
import pandas as pd

# Function to fetch minutes played for a single player in the current season
def get_player_minutes(player_name='Nikola Jokic', season='2023-24'):
    # Fetch player game logs (season type is Regular Season)
    player_game_log = playergamelog.PlayerGameLog(player_name=player_name, season=season, season_type='Regular Season')
    
    # Extract the data as a DataFrame
    df = player_game_log.get_data_frames()[0]
    
    # Filter relevant columns: GAME_DATE and MINUTES (MIN)
    df_filtered = df[['GAME_DATE', 'MIN']]
    
    # Calculate the total minutes played in the season
    total_minutes = df_filtered['MIN'].sum()
    
    return total_minutes, df_filtered

# Fetch Nikola Jokić's minutes played in the 2023-24 season
total_minutes, game_log_df = get_player_minutes()

# Show total minutes played
print(f"Total minutes played by Nikola Jokić: {total_minutes} minutes")

# Show the game log with minutes played
print(game_log_df.head())
