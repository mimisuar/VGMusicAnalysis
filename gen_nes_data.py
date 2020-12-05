from typing import Dict
import vgmusic, random
from collections import Counter
from music21 import note, stream
import json

SONG_LIMIT = 50
CONSOLE = "nes"
OUTPUTFILE = "test_output/nes.json"

def init_genre_data() -> Dict:
    return {
        "highest_pitch": Counter(),
        "lowest_pitch": Counter(),
        "rest_to_notes": 0.0
    }

def add_genre_data(dict1, dict2):
    res = init_genre_data()
    for key in dict1:
        res[key] = dict1[key] + dict2[key]
    return res

def process_stream(song_stream: stream.Stream) -> Dict:
    highest_pitch = None
    lowest_pitch = None
    note_count = 0
    rest_count = 0
    for note in song_stream.flat.getElementsByClass("GeneralNote"):
        if "Note" in note.classes:
            if not highest_pitch:
                highest_pitch = note.pitch
            else:
                if note.pitch > highest_pitch:
                    highest_pitch = note.pitch
            if not lowest_pitch:
                lowest_pitch = note.pitch
            else:
                if note.pitch < lowest_pitch:
                    lowest_pitch = note.pitch
            note_count += 1
        elif "Rest" in note.classes:
            rest_count += 1
    
    tmp = init_genre_data()
    if lowest_pitch:
        tmp["lowest_pitch"][lowest_pitch.nameWithOctave] += 1
    if highest_pitch:
        tmp["highest_pitch"][highest_pitch.nameWithOctave] += 1
    if note_count > 0:
        tmp["rest_to_notes"] = rest_count / note_count
    return tmp

def calc_nes_data():
    nes_data = {}
    nes_games = [game for game in vgmusic.get_games_by_console(CONSOLE)]
    loaded_song_count = 0
    genre_counter = Counter()
    for game in nes_games:
        
        if len(game.genres) > 0:
            print(game.name)
            for song in game.fetch_all_songs():
                song_data = process_stream(song)

                for genre in game.genres:
                    if genre not in nes_data:
                        nes_data[genre] = init_genre_data()
                    nes_data[genre] = add_genre_data(nes_data[genre], song_data)
                    genre_counter[genre] += 1
                break

    for genre in nes_data:
        nes_data[genre]["highest_pitch"] = nes_data[genre]["highest_pitch"].most_common(2)
        nes_data[genre]["lowest_pitch"] = nes_data[genre]["lowest_pitch"].most_common(2)
        if "rests_to_notes" in nes_data:
            nes_data[genre]["rests_to_notes"] /= genre_counter[genre]
    with open(OUTPUTFILE, "w") as f:
        f.write(json.dumps(nes_data, indent=4))

def calc_for_unknown_game(game_name):
    for tmp_game_name in vgmusic.get_game_names():
        if tmp_game_name == game_name:
            game = vgmusic.get_game_by_name(tmp_game_name)
            break
    else:
        return

    game_data = init_genre_data()
    song_count = 0
    for song in game.fetch_all_songs():
        song_data = process_stream(song)
        game_data = add_genre_data(game_data, song_data)
        song_count += 1
    game_data["highest_pitch"] = game_data["highest_pitch"].most_common(2)
    game_data["lowest_pitch"] = game_data["lowest_pitch"].most_common(2)
    if "rests_to_notes" in game_data:
        game_data["rests_to_notes"] /= song_count

    with open("test_output/{}.json".format(game_name), "w") as f:
        f.write(json.dumps(game_data, indent=4))

    


if __name__ == "__main__":
    calc_for_unknown_game("Mike_Tysons_Punchout")