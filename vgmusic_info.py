"""
This module adds some functions needed for crawling IGDB to add some information to the games.
"""
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult, GenreResult
from datetime import datetime
import requests
import json
import vgmusic_config as vgconfig
import os

auth_url = "https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials"
genre_ids = None
theme_ids = None

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

def generate_genres(creds=None):
    global genre_ids
    if isinstance(genre_ids, dict):
        return

    if os.path.isfile(vgconfig.genres_file):
        with open(vgconfig.genres_file, "r") as f:
            genre_ids = json.loads(f.read())
            return

    wrapper = IGDBWrapper(creds["client_id"], creds["access_token"])
    byte_array = wrapper.api_request(
        'genres',
        'fields name; limit 100;'
    )

    with open(vgconfig.genres_file, "wb") as f:
        f.write(byte_array)

    genre_ids = json.loads(byte_array)

def generate_themes(creds=None):
    global theme_ids
    if isinstance(theme_ids, dict):
        return

    if os.path.isfile(vgconfig.themes_file):
        with open(vgconfig.themes_file, "r") as f:
            theme_ids = json.loads(f.read())
            return

    wrapper = IGDBWrapper(creds["client_id"], creds["access_token"])
    byte_array = wrapper.api_request(
        'themes',
        'fields name; limit 100;'
    )

    with open(vgconfig.themes_file, "wb") as f:
        f.write(byte_array)
    
    theme_ids = json.loads(byte_array)

def add_game_info():
    creds = get_credentials()

    generate_genres(creds)
    generate_themes(creds)

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
                'fields name, first_release_date, genres, themes; search "{}"; limit 1;'.format(game_title.replace("_", " "))
            )
            #game_message = json.loads(byte_array)
            game_message = GameResult()
            game_message.ParseFromString(byte_array)
            if len(game_message.games) > 0:
                game_to_copy = game_message.games[0]
                game_to_edit = vgconfig.games[game_title]

                game_to_edit["id"] = game_to_copy.id
                game_to_edit["year"] = int(datetime.fromtimestamp(game_to_copy.first_release_date.seconds).strftime("%Y"))
                game_to_edit["themes"] = theme_ids_to_names(game_to_copy.themes)
                game_to_edit["genres"] = genre_ids_to_names(game_to_copy.genres)
                print("Updating {}.".format(game_title))
            
            #with open(file_name, "w") as file:
            #    file.write(json.dumps(response, indent=4))
            #    print("Wrote output to {}".format(file_name))
        except Exception as e:
            print("An error has occured: {}".format(str(e)))
    
    with open("games.json", "w") as games_file:
        games_file.write(json.dumps(vgconfig.games, indent=4, sort_keys=True))

def genre_ids_to_names(genre_list):
    names = []
    for genre in genre_list:
        for genre_info in genre_ids:
            if genre_info["id"] == genre.id:
                names.append(genre_info["name"])
    return names

def theme_ids_to_names(theme_list):
    names = []
    for theme in theme_list:
        for theme_info in theme_ids:
            if theme_info["id"] == theme.id:
                names.append(theme_info["name"])
    return names

if __name__ == "__main__":

    vgconfig.verify()
    
    start_time = datetime.now()
    add_game_info()
    end_time = datetime.now()
    dt = end_time - start_time
    ms = int(dt.total_seconds() * 1000)
    print("Took {} ms".format(ms))
    #pass
    #generate_genre_ids()