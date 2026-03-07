import requests 

def check_response(ruvesponse, message = None):
    if message == None:
        message = "Request failed."

    if response.status_code != 200:
        raise RuntimeError(f"{message} Error code: {response.status_code}")

if "sleeper_players" not in locals():
    response = requests.get("https://api.sleeper.app/v1/players/nfl")
    check_response(response, "Failed to fetch player data.")
    sleeper_players = response.json()

    username = "ARoth13"

response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
check_response(response, "Failed to fetch user data.")
user_id = response.json()["user_id"]


response = requests.get(f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/2023")
check_response(response, "Failed to fetch league data.")
league_json = response.json()