import vgmusic
import vgmusic_config as config
import json

GAME_CHECKPOINT = 50 # save the file after every 10 games

def validate_files(forced):
    counter = GAME_CHECKPOINT

    for game_name in vgmusic.get_game_names():
        game = vgmusic.get_game(game_name)

            

        for song_title in vgmusic.get_songs_by_game(game_name):
            if game["songs"][song_title] == True:
                continue

            try:
                print("{0}/{1} loaded!".format(game_name, song_title))
                stream = vgmusic.fetch(game_name, song_title)
                url = game["songs"][song_title]
                game["songs"][song_title] = {
                    "url": url,
                    "loadable": True
                }
                counter -= 1
            except Exception as e:
                print(str(e))
                url = game["songs"][song_title]
                game["songs"][song_title] = {
                    "url": url,
                    "loadable": False
                }
        
        game.pop("loadable", None)
        
        if counter <= 0:
            counter = GAME_CHECKPOINT
            print("Saving to file...")
            with open("{}".format(config.games_file), "w") as f:
                f.write(json.dumps(config.games, indent=4, sort_keys=True))

    with open("{}".format(config.games_file), "w") as f:
        f.write(json.dumps(config.games, indent=4, sort_keys=True))

if __name__ == "__main__":
    import sys
    forced = False
    if "--force" in sys.argv:
        forced = True
    validate_files(forced)
    
    