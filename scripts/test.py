import os, sys
sys.path.append(os.getcwd())
import vgmdb, json, vgmdb.platform
import vgmdb.genre.constants as genres

db = vgmdb.Database.get_default_database()
for game in db.get_games():
    if game.has_genre(genres.Fighting):
        print(game.name)