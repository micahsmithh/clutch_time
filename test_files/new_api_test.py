from nba_api.stats.endpoints import boxscoretraditionalv2, boxscoretraditionalv3, teamgamelog
from nba_api.stats.static import players, teams
import pandas as pd






def get_starters(team_id):
    season = '2025' 
    team = next((team['abbreviation'] for team in teams.get_teams() if team['id'] == team_id), None) # get abbreivation from team_id

    # Get regular season game log
    gamelog_regular = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Regular Season')
    games_regular = gamelog_regular.get_data_frames()[0]

    # Get playoff game log
    gamelog_playoffs = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star='Playoffs')
    games_playoffs = gamelog_playoffs.get_data_frames()[0]

    # Combine into one data frame
    games_combined = pd.concat([games_regular, games_playoffs], ignore_index=True)

    # Sort the combined games by GAME_DATE to get the most recent game
    games_combined['GAME_DATE'] = pd.to_datetime(games_combined['GAME_DATE'])  # first ahave to convert to datatime format
    games_combined_sorted = games_combined.sort_values(by='GAME_DATE', ascending=False)

    # Get most recent game
    if not games_combined_sorted.empty:
        for _, game in games_combined_sorted.iterrows():
            game_id = game['Game_ID']
            print(f"Checking Game ID: {game_id}")
            
            # Fetch the box score for the current game
            boxscore = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)

            # Get player stats DataFrame
            player_df = boxscore.player_stats.get_data_frame()
            team_sb_df = boxscore.team_starter_bench_stats.get_data_frame()
            print("Box Score")
            print(team_sb_df.head())  # Display the first few rows of player stats for debugging
            

            # Filter players to be only starters from selected team
            team_starters = player_stats[
                (player_df['teamTricode'] == team) &
                (player_df['startersBench'] == 'Starter')
            ]

            # Once team starters are found: display (For games at end of season, often no starters are listed since many players are resting)
            if not team_starters.empty:
                print(f"Found starters for Game ID: {game_id}")
                print(team_starters[['PLAYER_NAME', 'START_POSITION']])
                return team_starters['PLAYER_NAME'].tolist()  # exit loops when starters are found
        else:
            print(f"No valid starters found in the recent games for {team}.")
            return
    else:
        print(f"No games found for {team}.")
        return
    

# Gets list of dictionaries (a dictionary for each nba team)
nba_teams = teams.get_teams()

# Map team abreviation to team ID
team_id_map = {team['abbreviation']: team['id'] for team in nba_teams} 

print(team_id_map['CLE'])

get_starters(team_id_map['CLE'])