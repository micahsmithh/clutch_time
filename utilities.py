from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import TeamEstimatedMetrics
from nba_api.stats.endpoints import TeamEstimatedMetrics, LeagueDashPlayerClutch, LeagueDashPlayerStats
import requests, time

# Gets team id from abbreviation using nba_api
def get_team_id_from_abbreviation(abbreviation):
        # Fetch the list of all NBA teams
        all_teams = teams.get_teams()
        
        # Search for the team with the given abbreviation
        for team in all_teams:
            if team['abbreviation'] == abbreviation:
                return team['id']
        
        # Return None if no match is found
        return None


# Gets team stats dictionary 
def get_team_stats_dict(team_name):
    # Define parameters
    season = '2024-25' 
    season_type = 'Regular Season'

    # Call the endpoint
    # try:
    #     stats = TeamEstimatedMetrics(season=season, season_type=season_type)

    #     # Get the data frame
    #     df = stats.get_data_frames()[0]
    # except requests.exceptions.ConnectionError:
    #     print("❌ Connection error: Check your internet or the NBA API server.")
    #     return
    
    for attempt in range(3):
        try:
            stats = TeamEstimatedMetrics(season=season, season_type=season_type)
            df = stats.get_data_frames()[0]
            break  # break out of loop if failed
        except requests.exceptions.ConnectionError:
            print(f"Attempt {attempt + 1} failed")
            time.sleep(2)
    else:
        print("❌ All retries failed.")
        df = None
        return

    # Filter for team
    team_row = df[df['TEAM_NAME'] == team_name]
    
    # Get E_TM_TOV_PCT
    if not team_row.empty:
        team_stats_dict = {
            'TOV_PCT' : team_row.iloc[0]['E_TM_TOV_PCT'],
            'OREB_PCT' : team_row.iloc[0]['E_OREB_PCT'],
            'DREB_PCT' : team_row.iloc[0]['E_DREB_PCT'],
        } 
        print(f"{team_name} stats {team_stats_dict}")
        return team_stats_dict
    elif team_name == "Los Angeles Clippers":
        team_row = df[df['TEAM_NAME'] == "LA Clippers"]

        team_stats_dict = {
            'TOV_PCT' : team_row.iloc[0]['E_TM_TOV_PCT'],
            'OREB_PCT' : team_row.iloc[0]['E_OREB_PCT'],
            'DREB_PCT' : team_row.iloc[0]['E_DREB_PCT'],
        } 
        print(f"LA Clippers stats {team_stats_dict}")
        return team_stats_dict
    else:
        print(f"{team_name} data not found")


# Gets clutch stats dictionary of inputted player
def get_clutch_dict(players_list):

    # pull clutch stats
    clutch_stats = LeagueDashPlayerClutch(
    season='2024-25',
    season_type_all_star='Regular Season',
    clutch_time='Last 5 Minutes', 
    ahead_behind='Ahead or Behind', 
    point_diff=5  # within 5 points
    )

    # Get Data Frame
    df = clutch_stats.get_data_frames()[0]

    clutch_dict = {}

    print(f"Team : {players_list}")

    for name in players_list:
        player_info = players.find_players_by_full_name(name)

        # Error Checking Names
        if not player_info:
            print(f"Player {name} not found")
            continue

        player_id = player_info[0]['id']
        player_clutch_stats = df[df['PLAYER_ID'] == player_id]

        # Error Checking Stats
        if player_clutch_stats.empty:
            print(f"Season stats not found for {name}")
            continue

        # calculate FG2_PCT
        #print(player_clutch_stats.iloc[0]['FGA'])

        two_points_attempted = player_clutch_stats.iloc[0]['FGA'] - player_clutch_stats.iloc[0]['FG3A']
        two_points_made = player_clutch_stats.iloc[0]['FGM'] - player_clutch_stats.iloc[0]['FG3M']
        two_point_percentage = round(two_points_made / two_points_attempted, 3) if two_points_attempted != 0 else 0 #zero checking

        clutch_dict[name] = {
            'FG_PCT' : player_clutch_stats.iloc[0]['FG_PCT'],
            'FG3_PCT' : player_clutch_stats.iloc[0]['FG3_PCT'],
            'FG2_PCT' : two_point_percentage,
            'FT_PCT'  : player_clutch_stats.iloc[0]['FT_PCT']
        
    }
        
    # print(f"{players_list[0]}'s FG_PCT = {clutch_dict[players_list[0]]['FG_PCT']}")
    # print(f"{players_list[0]}'s FG2_PCT = {clutch_dict[players_list[0]]['FG2_PCT']}")
    # print(f"{players_list[0]}'s FG3_PCT = {clutch_dict[players_list[0]]['FG3_PCT']}")
    # print(f"{players_list[0]}'s FT_PCT = {clutch_dict[players_list[0]]['FT_PCT']}")
    print("CLUTCH")
    return clutch_dict

# Gets regular season stats dictionary of inputted player
def get_regular_season_dict(players_list):
    # Pull regular season player stats
    regular_stats = LeagueDashPlayerStats(
        season='2024-25',
        season_type_all_star='Regular Season'
    )

    # Get Data Frame
    df = regular_stats.get_data_frames()[0]

    player_stats_dict = {}

    print(f"Team : {players_list}")

    for name in players_list:
        player_info = players.find_players_by_full_name(name)

        # Error Checking Names
        if not player_info:
            print(f"Player {name} not found")
            continue

        player_id = player_info[0]['id']
        player_season_stats = df[df['PLAYER_ID'] == player_id]

        # Error Checking Stats
        if player_season_stats.empty:
            print(f"Season stats not found for {name}")
            continue

        # calculate FG2_PCT
        #print(player_season_stats.iloc[0]['FGA'])

        two_points_attempted = player_season_stats.iloc[0]['FGA'] - player_season_stats.iloc[0]['FG3A']
        two_points_made = player_season_stats.iloc[0]['FGM'] - player_season_stats.iloc[0]['FG3M']
        two_point_percentage = round(two_points_made / two_points_attempted, 3) if two_points_attempted != 0 else 0 # zero checking

        player_stats_dict[name] = {
            'FG_PCT' : player_season_stats.iloc[0]['FG_PCT'],
            'FG3_PCT' : player_season_stats.iloc[0]['FG3_PCT'],
            'FG2_PCT' : two_point_percentage,
            'FT_PCT'  : player_season_stats.iloc[0]['FT_PCT']
        
    }
    print("REGULAR")
    return player_stats_dict


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