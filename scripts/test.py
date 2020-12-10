import os, sys
sys.path.append(os.getcwd())
import vgmdb, json, vgmdb.platform
import vgmdb.theme.constants as themes
from music21 import converter

db = vgmdb.Database.get_default_database()
for game in db.get_games():
    if game.has_theme(themes.Romance):
        for song in game.get_songs():
            song_path = song.fetch()