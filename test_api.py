from nba_api.stats.endpoints import LeagueGameFinder, BoxScoreAdvancedV2
from nba_api.stats.static import teams
import numpy as np
import time  # To handle rate limiting

# Get Cleveland's team ID
cle_team = teams.find_team_by_abbreviation('OKC')
cle_team_id = cle_team['id']

# Define the season
season = '2024-25'

# Get all games for Cleveland
game_finder = LeagueGameFinder(team_id_nullable=cle_team_id, season_nullable=season)
games_data = game_finder.get_data_frames()[0]  # This returns a pandas DataFrame

# Get unique game IDs
game_ids = games_data['GAME_ID'].unique()

turnover_percentages = []

for game_id in game_ids:
    try:
        # Fetch the advanced box score data
        boxscore = BoxScoreAdvancedV2(game_id=game_id, start_period=1, end_period=4, start_range=0, end_range=2880)
        team_stats = boxscore.get_data_frames()[1]  # 1 = TeamStats
        cle_stats = team_stats[team_stats['TEAM_ID'] == cle_team_id]
        
        # Get the turnover percentage
        tov_pct = cle_stats.iloc[0]['TM_TOV_PCT']
        turnover_percentages.append(tov_pct)
        
        time.sleep(0.6)  # To avoid hitting rate limits
    except Exception as e:
        print(f"Error processing game {game_id}: {e}")

# Calculate and print season average
if turnover_percentages:
    avg_tov_pct = np.mean(turnover_percentages)
    print(f"Cleveland's average turnover percentage for {season}: {avg_tov_pct:.2f}%")
else:
    print("No data available.")
