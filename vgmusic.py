""" 
Public API for interacting with VGMusic database. 
"""
import vginfo, vgconfig
from music21 import converter, stream
from typing import Generator, Dict, List

def fetch(game_name: str, song_title: str) -> stream.Stream:
    """
    Returns a stream of the given song. Raises exception on error. 
    """

    file_path = vgconfig.cache_name + "/" + game_name + "/" + song_title + ".mid"
    try:
        
        song_stream = converter.parse(file_path)
    except Exception as e:
        v = Exception()
        v.args = "Unable to parse {0}/{1}: {2}".format(game_name, song_title, str(e))
        raise v
    return song_stream

def get_songs_by_game(game_name: str) -> Generator[str, None, None]:
    """ 
    Iterates through all of the songs in a game. 
    """
    for song_title in vgconfig.games[game_name]["songs"]:
        yield song_title

def get_game_names() -> Generator[str, None, None]:
    """ 
    Iterates through all of the game names. 
    """
    yield from vgconfig.games

# see games.json for what this dictionary looks like. 
def get_game(game_name: str) -> Dict:
    """ 
    The get all of the information on a given name. Raises exception on error.
    """
    assert game_name in vgconfig.games, "Game '{}' not defined in vgconfig.".format(str(game_name))
    return vgconfig.games[game_name]

def get_genre_names() -> Generator[str, None, None]:
    """ 
    Iterators through all the genre names. 
    """
    vginfo.generate_genres()

    for genre_dict in vginfo.genre_ids:
        yield genre_dict["name"]

def get_themes_names() -> Generator[str, None, None]:
    """ 
    Iterators through all the theme names. 
    """
    vginfo.generate_themes()

    for genre_dict in vginfo.theme_ids:
        yield genre_dict["name"]

def get_games_by_genre(genre_name: str) -> Generator[str, None, None]:
    """ 
    Iterates through all of the game titles which contain a given genre. 
    """
    for game_name in get_game_names():
        game = get_game(game_name)

        if genre_name in game["genres"]:
            yield game_name

def get_games_by_genres(genre_list: List[str]) -> None:
    """ 
    Iterates through all of the game titles which contain all of the given genres. 
    """
    for game_name in get_game_names():
        game = get_game(game_name)

        for genre_name in genre_list:
            if genre_name not in game["genres"]:
                break
        else:
            yield game_name

def get_games_by_theme(theme_name: str) -> Generator[str, None, None]:
    """ 
    Iterates through all of the game titles which contain a given theme. 
    """
    for game_name in get_game_names():
        game = get_game(game_name)

        if theme_name in game["themes"]:
            yield game_name

def get_games_by_themes(theme_list: List[str]) -> Generator[str, None, None]:
    """ 
    Iterates through all of the game titles which contain all of the given themes. 
    """
    for game_name in get_game_names():
        game = get_game(game_name)

        for theme_name in theme_list:
            if theme_name not in game["themes"]:
                break
        else:
            yield game_name

# initialization code here:
vgconfig.verify()