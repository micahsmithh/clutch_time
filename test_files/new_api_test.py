from nba_api.stats.endpoints import boxscoretraditionalv2, boxscoretraditionalv3, teamgamelog
from nba_api.stats.static import players, teams
import pandas as pd
import requests

def request_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.nba.com/",
        "Origin": "https://www.nba.com",
        "Accept": "application/json, text/plain, */*"
    }

    print("Requesting...")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request failed: {response.status_code}")
        print(response.text)
        return None
    else:
        try:
            data = response.json()
            print("JSON parsed successfully.")
            return data
        except Exception as e:
            print("Failed to parse JSON.")
            print(response.text)
            return None






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
            

            boxscore_data = request_data(f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json")
            
            home_tricode = boxscore_data["game"]["homeTeam"]["teamTricode"]
            
            # Check teamm
            if home_tricode == team:
                which_team = "homeTeam"
            else:
                which_team = "awayTeam"

            # Get starters
            team_starters = [ 
                    player for player in boxscore_data["game"][which_team]["players"] if player["starter"] == "1"
                ]

            starters_list = [player['name'] for player in team_starters]


            print(starters_list)

            if starters_list:
                print(f"Found starters for Game ID: {game_id}")
                for player in team_starters:
                    print(player['name'], player['position'])
                return starters_list

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

#print(team_id_map['CLE'])

starters = get_starters(team_id_map['CLE'])

print(starters)