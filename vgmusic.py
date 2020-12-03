import vgdownloader as vgd
import vgconfig as config # I'm too lazy to change now :/
from music21 import converter

def fetch(game_name, song_title=None):
    """
    Returns a stream of the given song, or None on failure.
    """
    if isinstance(game_name, tuple):
        assert len(game_name) == 2
        assert isinstance(game_name[0], str)
        assert isinstance(game_name[1], str)
        song_title = game_name[1]
        game_name = game_name[0]

    file_path = config.cache_name + "/" + game_name + "/" + song_title + ".mid"
    try:
        
        song_stream = converter.parse(file_path)
    except Exception as e:
        print(str(e))
        return None
    return song_stream

def get_all_songs():
    for game_name in config.games:
        for song_name in config.games[game_name]["songs"]:
            yield (game_name, song_name)

def get_songs_by_game(game_name):
    for song_title in config.games[game_name]["songs"]:
        yield song_title

def get_games_by_name(name):
    for game_name in config.games:
        if name in game_name:
            yield game_name

def get_game_names():
    yield from config.games

def get_game(game_name):
    assert game_name in config.games, "Game '{}' not defined in vgconfig.".format(str(game_name))
    return config.games[game_name]