import vgmusic
from vgmusic_game import Game

for game_title in vgmusic.get_game_names():
    my_game = Game(game_title, vgmusic.get_game(game_title))
    if my_game.loadable:
        print("{} is loadable.".format(game_title))
        for stream in my_game.fetch_all_songs():
            pass
