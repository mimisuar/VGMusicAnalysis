import vgmusic, random

SONG_LIMIT = 50
loaded_song_count = 0
CONSOLE = "nes"
OUTPUTFILE = "test_output/nes.json"

nes_data = {
    "highest_note": None,
    "lowest_note": None
}
nes_games = [game for game in vgmusic.get_games_by_console(CONSOLE)]
random.shuffle(nes_games)
for game in nes_games:
    done = False
    for song_title in game.loadable:
        if game.loadable[song_title]:
            print(song_title)
            loaded_song_count += 1
            if loaded_song_count == 50:
                done = True
                break
    if done:
        break
            