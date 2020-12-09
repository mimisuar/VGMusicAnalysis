from bs4 import BeautifulSoup
from igdb.wrapper import IGDBWrapper
from igdb.igdbapi_pb2 import GameResult
import datetime
import requests
import json
import vgmdb

BASE_URL = "http://vgmusic.com"
AUTH_URL = "https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials"

wrapper = None

def simplify(obj) -> str:
    return str(obj).lower().replace("\"", "").replace("(", "").replace(")", "").replace("/", " ").replace("\\", " ").replace("?", " ").replace("_", " ")

def get_credentials(force_auth:bool=False) -> list:
    with open("secrets/igdb_auth.json", "r") as auth_file:
        creds = json.loads(auth_file.read())
    if force_auth or creds["access_token"] == "":
        print("Authenticating with server.")
        response = requests.post(AUTH_URL.format(creds["client_id"], creds["secret"]))
        if response.status_code == requests.codes.ok:
            response_json = json.loads(response.text)
            creds["access_token"] = response_json["access_token"]
            with open("secrets/igdb_auth.json", "w") as auth_file:
                auth_file.write(json.dumps(creds))
    return creds

def find_game_info(game_title: str) -> GameResult:
    global wrapper
    if not wrapper:
        creds = get_credentials()
        wrapper = IGDBWrapper(creds["client_id"], creds["access_token"])
    
    byte_array = wrapper.api_request(
                'games.pb',
                'fields name, first_release_date, genres, themes, platforms; search "{}"; limit 1;'.format(game_title)
            )
    game_message = GameResult()
    game_message.ParseFromString(byte_array)
    if len(game_message.games) > 0:
        return game_message.games[0]
    return None

def generate_database() -> vgmdb.Database:
    #config_games = {}
    db = vgmdb.Database()

    r = requests.get(BASE_URL)
    if r.status_code == requests.codes.ok:
        html_doc = BeautifulSoup(r.text, "html.parser")

        for link in html_doc.find_all("a"):
            if "console" in link["href"]:
                console_name = simplify(link.string)
                # crawl through the music now :)
                console_url = BASE_URL + str(link["href"])[1:]
                sub_r = requests.get(console_url)
                if sub_r.status_code == requests.codes.ok:
                    console_doc = BeautifulSoup(sub_r.text, "html.parser")
                    game = None
                    for sub_link in console_doc.find_all("a"):
                        name = sub_link.get("name")
                        if name:
                            game = vgmdb.Game()
                            db.add_game(game)
                            #config_games[game_name] = {"console": console_name, "year": 2000, "songs": {}, "genres": [], "themes": [], "id": 0}
                            print("Adding {}...".format(name))
                            game.name = simplify(name)
                            game_message = find_game_info(game.name)
                            if game_message:
                                for theme_id in game_message.themes:
                                    game.add_theme(vgmdb.Theme(theme_id.id))
                                for genre_id in game_message.genres:
                                    game.add_genre(vgmdb.Genre(genre_id.id))
                                for platform_id in game_message.platforms:
                                    game.add_platform(vgmdb.Platform(platform_id.id))
                                game.year = int(datetime.datetime.fromtimestamp(game_message.first_release_date.seconds).strftime("%Y"))
                                game.id = game_message.id

                            

                        elif ".mid" in sub_link["href"]:
                            song_name = simplify(sub_link.string)
                            #print(game_name + "/" + song_name + ": "+ sub_link["href"])
                            song_url = console_url + str(sub_link["href"])
                            game.add_song(song_name, song_url)
    else:
        r.raise_for_status()

    return db

if __name__ == "__main__":
    db = generate_database()
    with open("vgmdb/data/games.json", "w") as f:
        json.dump(db.encode(), f, indent=4)