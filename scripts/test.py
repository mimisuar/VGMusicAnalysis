import os, sys
sys.path.append(os.getcwd())
import vgmdb, json, vgmdb.platform

db = vgmdb.Database.get_default_database()