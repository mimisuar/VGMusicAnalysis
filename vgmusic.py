""" 
Public API for interacting with VGMusic database.
"""
import vgmusic_config as vgconfig
import vgmusic_info as vginfo
from vgmusic_game import Game
from music21 import converter, stream
from typing import Generator, Dict, List, Union

def fetch(game_name: str, song_title: str) -> stream.Stream:
    """
    Returns a stream of the given song. Raises exception on error. 
    """

    file_path = vgconfig.cache_name + "/" + game_name + "/" + song_title + ".mid"
    try:
        
        song_stream = converter.parse(file_path)
    except Exception as e:
        raise Exception("Unable to parse {0}/{1}: {2}".format(game_name, song_title, str(e)))
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

def get_games() -> Generator[Game, None, None]:
    for game_name in vgconfig.games:
        yield Game(game_name, vgconfig.games[game_name])

def get_games_by_console(console: str) -> Generator[Game, None, None]:
    for game in get_games():
        if game.console == console:
            yield game

def get_games_by_genres(genres: Union[str, List[str]]) -> Generator[Game, None, None]:
    for game in get_games():
        if game.has_genres(genres):
            yield game

def get_games_by_themes(themes: Union[str, List[str]]) -> Generator[Game, None, None]:
    for game in get_games():
        if game.has_themes(themes):
            yield game

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

# initialization code here:
vgconfig.verify()