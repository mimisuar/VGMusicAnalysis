"""
This module adds some functions needed for crawling IGDB to add some information to the games.
"""
from igdb.wrapper import IGDBWrapper
import requests
import json

auth_url = "https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials"

def get_credentials():
    with open("secrets/igdb_auth.json", "r") as auth_file:
        creds = json.loads(auth_file.read())
    if creds["access_token"] == "":
        print("Authenticating with server.")
        response = requests.post(auth_url.format(creds["client_id"], creds["secret"]))
        if response.status_code == requests.codes.ok:
            response_json = json.loads(response.text)
            creds["access_token"] = response_json["access_token"]
            with open("secrets/igdb_auth.json", "w") as auth_file:
                auth_file.write(json.dumps(creds))
    return creds

def add_game_info():
    creds = get_credentials()
    wrapper = IGDBWrapper(creds["client_id"], creds["access_token"])
    byte_array = wrapper.api_request(
            'games',
            "fields *;")
    response = json.loads(byte_array)
    with open("output.json", "w") as file:
        file.write(json.dumps(response, indent=4))

if __name__ == "__main__":
    add_game_info()