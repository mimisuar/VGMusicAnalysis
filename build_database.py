from bs4 import BeautifulSoup
import requests
import json
import vgmdb

def simplify(obj) -> str:
    return str(obj).lower().replace("\"", "").replace("(", "").replace(")", "").replace("/", " ").replace("\\", " ").replace("?", " ").replace("_", " ")

BASE_URL = "http://vgmusic.com"

def fetch_info_from_igdb():
    pass

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
                            game.name = simplify(name)
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
    with open("db.json", "w") as f:
        json.dump(db.encode(), f, indent=4)