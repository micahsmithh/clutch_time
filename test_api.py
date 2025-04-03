import pandas as pd
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
from nba_api.stats.static import players
from datetime import datetime

# Nikola Jokić
player = players.find_players_by_full_name("Lebron James")

#extra id
player_id = player[0]['id']

career = playercareerstats.PlayerCareerStats(player_id=player_id) 

# get player info for Jokic
player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
player_name = player_info.get_data_frames()[0]['DISPLAY_FIRST_LAST'][0]


dob_str = player_info.get_data_frames()[0]['BIRTHDATE'][0]  # Format: '1995-02-19T00:00:00'

# Convert DOB string to datetime object
dob = datetime.strptime(dob_str.split('T')[0], "%Y-%m-%d")

# Calculate age
today = datetime.today()
player_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


print(f"{player_name}'s age = {player_age}")

# pandas data frames (optional: pip install pandas)
career.get_data_frames()[0]

# json
career.get_json()

# dictionary
career.get_dict()

df = career.get_data_frames()[0]

# Display the first few rows
#print(df.head())

latest_season = df.iloc[-1]


# Access specific columns
#print(latest_season[['SEASON_ID', 'PPG']])  # Example: Points, Assists, Rebounds per season

rookie = df.iloc[0]
latest = df.iloc[-1]

rookie_ppg = rookie['PTS'] / rookie['GP']
rookie_apg = rookie['AST'] / rookie['GP']
rookie_rpg = rookie['REB'] / rookie['GP']

latest_ppg = latest['PTS'] / latest['GP']
latest_apg = latest['AST'] / latest['GP']
latest_rpg = latest['REB'] / latest['GP']



print(f"{player_name}'s Rookie Season ({rookie['SEASON_ID']}): {rookie_ppg:.1f} PPG, {rookie_apg:.1f} APG, {rookie_rpg:.1f} RPG")
print(f"{player_name}'s Latest Season ({latest['SEASON_ID']}): {latest_ppg:.1f} PPG, {latest_apg:.1f} APG, {latest_rpg:.1f} RPG")



#print(f"Rookie Year ({rookie['SEASON_ID']}): {rookie['PTS'] } PPG, {rookie['AST']} APG, {rookie['REB']} RPG")
#print(f"Latest Year ({latest['SEASON_ID']}): {latest['PTS']} PPG, {latest['AST']} APG, {latest['REB']} RPG")


#make function which fetchs player framework
#function that fetches clutch stats