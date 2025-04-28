from nba_api.stats.endpoints import teamgamelog, boxscoretraditionalv2
from nba_api.stats.static import teams
import pandas as pd

def get_team_id_from_abbreviation(abbreviation):
    # Fetch the list of all NBA teams
    all_teams = teams.get_teams()
    
    # Search for the team with the given abbreviation
    for team in all_teams:
        if team['abbreviation'] == abbreviation:
            return team['id']
    
    # If no match is found, return None
    return None



team = 'CLE'
team_id = get_team_id_from_abbreviation(team)  # Cleveland Cavaliers
season = '2024'  # 2024 season (you can change this to the relevant season)

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

        team_starters = player_stats[
            (player_stats['TEAM_ABBREVIATION'] == team) &
            (player_stats['START_POSITION'].isin(['G', 'F', 'C']))
        ]

        # Filter players who have a non-null START_POSITION (they are the starters)
        # for _, player in player_stats.iterrows():
        #     if player['TEAM_ABBREVIATION'] == team and player['START_POSITION'] in ['G', 'F', 'C'] :
        #         team_starters._append(player)
        #starters = player_stats[player_stats['START_POSITION'].notnull()]

        # Further filter by team (optional, if you want just Cavs)
        #team_starters = starters[starters['TEAM_ABBREVIATION'] == team]

        # If team_starters is not empty, display the starting 5 and break out of the loop
        if not team_starters.empty:
            print(f"Found starters for Game ID: {game_id}")
            print(f"Game details:\n{game}")
            print(f"Game ID = {game_id}")
            print(team_starters[['PLAYER_NAME', 'START_POSITION']])
            break  # exit loops when starters are found
    else:
        print(f"No valid starters found in the recent games for {team}.")
else:
    print(f"No games found for {team}.")
