"""
This module adds some functions needed for crawling IGDB to add some information to the games.
"""
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult, Genre
from datetime import datetime
import requests
import json
import vgconfig

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
    #byte_array = wrapper.api_request(
    #        'games',
    #        'fields *; search "sonic the hedgehog"; limit 5;')
    #response = json.loads(byte_array)

    for game_title in vgconfig.games:
        file_name = "test_output\\{}.json".format(game_title)

        try:
            byte_array = wrapper.api_request(
                'games.pb',
                'fields name, first_release_date, genres; search "{}"; limit 1;'.format(game_title.replace("_", " "))
            )
            #game_message = json.loads(byte_array)
            game_message = GameResult()
            game_message.ParseFromString(byte_array)
            if len(game_message.games) > 0:
                game_to_copy = game_message.games[0]
                game_to_edit = vgconfig.games[game_title]

                game_to_edit["id"] = game_to_copy.id
                game_to_edit["year"] = int(datetime.fromtimestamp(game_to_copy.first_release_date.seconds).strftime("%Y"))
            else:
                #print("No matches found for '{}'.".format(game_title.replace("_", " ")))
                pass
            
            #with open(file_name, "w") as file:
            #    file.write(json.dumps(response, indent=4))
            #    print("Wrote output to {}".format(file_name))
        except Exception as e:
            print("An error has occured: {}".format(str(e)))
    
    with open("games.json", "w") as games_file:
        games_file.write(json.dumps(vgconfig.games))

if __name__ == "__main__":
    vgconfig.verify()
    add_game_info()