import os, sys
sys.path.append(os.getcwd())
import vgmdb, json, vgmdb.platform

db = vgmdb.Database.get_default_database()
nes = vgmdb.Platform.get_platform_by_abbr("nes")

for game in db.get_games():
    if not game.has_platform(nes):
        continue

    print(game._genres)