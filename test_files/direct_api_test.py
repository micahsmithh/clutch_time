import requests

def request_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.nba.com/",
        "Origin": "https://www.nba.com",
        "Accept": "application/json, text/plain, */*"
    }

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
        

url = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_0042500304.json"

data = request_data(url)



game = data["game"]
print(f"Game keys: {list(game.keys())}")

homeTeam = game["homeTeam"]
print(f"Home team keys: {list(homeTeam.keys())}")


players = homeTeam["players"]
print(f"Player keys within list: {list(players[0].keys())}")  # Print keys of the players dictionary

print(players[0]["starter"])  # Print the family name of the first player

for player in players:
    print(f"Player: {player['firstName']} {player['familyName']}, Starter: {player['starter']}")

print(players[0]["statistics"].keys())  # Print the points of the first player

# print(game)


home_tricode = data["game"]["homeTeam"]["teamTricode"]

# print(f"Home team tricode: {home_tricode}")

if home_tricode == "CLE":
    team_starters = [ 
        player for player in data["game"]["homeTeam"]["players"] if player["starter"] == "1"
    ]


print(data["game"]["homeTeam"]["players"][0]["starter"])


for player in team_starters:
    print(player['name'])

players_list = [player['name'] for player in team_starters]


print(players_list)

# url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

# data2 = request_data(url)

# print(data2.keys())  # Print the top-level keys of the JSON data

# scoreboard = data2["scoreboard"]
# print(scoreboard.keys())  # Print the keys of the scoreboard dictionary

# games = scoreboard["gameDate"]
# print(games)




# url = "https://stats.nba.com/stats/scoreboardv2"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Origin": "https://www.nba.com",
#     "Referer": "https://www.nba.com/",
#     "Connection": "keep-alive"
# }

# response = requests.get(url, headers=headers)

# print("Status:", response.status_code)

# data = response
# print(type(data))
# print(data)