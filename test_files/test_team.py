from nba_api.stats.endpoints import commonteamroster

team_id = 1610612747  # Los Angeles Lakers

# Fetch the team's roster
roster = commonteamroster.CommonTeamRoster(team_id=team_id)

# Convert to DataFrame
df = roster.get_data_frames()[0]

# Print all column names
print(df[["TeamID", "PLAYER"]])


players = df["PLAYER"].tolist()