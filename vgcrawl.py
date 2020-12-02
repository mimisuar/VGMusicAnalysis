from bs4 import BeautifulSoup
from igdb.wrapper import IGDBWrapper
import requests
import json

base_url = "http://vgmusic.com"

def simplify(obj) -> str:
    return str(obj).lower().replace(" ", "").replace("_", "").replace("\"", "").replace("(", "").replace(")", "")

def parse_vgmusic():
    config_games = {}

    r = requests.get(base_url)
    if r.status_code == requests.codes.ok:
        html_doc = BeautifulSoup(r.text, "html.parser")

        for link in html_doc.find_all("a"):
            if "console" in link["href"]:
                console_name = simplify(link.string)
                # crawl through the music now :)
                console_url = base_url + str(link["href"])[1:]
                sub_r = requests.get(console_url)
                if sub_r.status_code == requests.codes.ok:
                    console_doc = BeautifulSoup(sub_r.text, "html.parser")
                    game_name = ""
                    for sub_link in console_doc.find_all("a"):
                        name = sub_link.get("name")
                        if name:
                            game_name = name

                            config_games[game_name] = {"console": console_name, "year": 2000, "origin": "None", "songs": {}, "genre": [], "theme": "None"}
                        elif ".mid" in sub_link["href"]:
                            song_name = simplify(sub_link.string)
                            #print(game_name + "/" + song_name + ": "+ sub_link["href"])
                            song_url = console_url + str(sub_link["href"])[1:]
                            config_games[game_name]["songs"][song_name] = song_url
    else:
        r.raise_for_status()

    with open("games.json", "w") as games:
        games.write(json.dumps(config_games, indent=4))

if __name__ == "__main__":
    #parse_vgmusic()
    with open("secrets/igbd_auth.json", "r") as auth_file:
        auth = json.loads(auth_file.read())

    auth_res = requests.post(
        "https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials".format(auth["client-id"], auth["token"]))

    if auth_res.status_code != requests.codes.ok:
        auth_res.raise_for_status()
    auth_data = json.loads(auth_res.text)

    print(auth_data)